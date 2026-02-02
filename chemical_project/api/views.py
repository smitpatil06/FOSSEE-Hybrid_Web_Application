import pandas as pd
import io
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .models import UploadBatch, EquipmentData
from .serializers import UploadBatchSerializer, EquipmentDataSerializer

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        try:
            df = pd.read_csv(file_obj)
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_columns):
                return Response({"error": f"Missing columns. Required: {required_columns}"}, status=400)
        except Exception as e:
            return Response({"error": f"CSV Parse Error: {str(e)}"}, status=400)

        # History Management: Keep only last 5 per user
        batches = UploadBatch.objects.filter(uploaded_by=request.user).order_by('uploaded_at')
        if batches.count() >= 5:
            batches.first().delete()

        batch = UploadBatch.objects.create(filename=file_obj.name, uploaded_by=request.user)

        equipment_list = [
            EquipmentData(
                batch=batch,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            ) for _, row in df.iterrows()
        ]
        EquipmentData.objects.bulk_create(equipment_list)

        return Response({"message": "Success", "batch_id": batch.id}, status=201)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Return user's own batches, most recent first
        batches = UploadBatch.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
        serializer = UploadBatchSerializer(batches, many=True)
        return Response(serializer.data)

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, batch_id):
        try:
            # Ensure user can only access their own batches
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            data = batch.equipment.all()
            
            stats = data.aggregate(
                avg_flow=Avg('flowrate'),
                avg_press=Avg('pressure'),
                total_count=Count('id')
            )
            
            # Create distribution for charts
            type_counts = {}
            for item in data:
                t = item.equipment_type
                type_counts[t] = type_counts.get(t, 0) + 1

            return Response({
                "id": batch.id,
                "filename": batch.filename,
                "summary": stats,
                "type_distribution": type_counts,
                "data": EquipmentDataSerializer(data, many=True).data
            })
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

    def delete(self, request, batch_id):
        """Allow users to delete their own upload batch and associated equipment records."""
        try:
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            batch.delete()
            return Response({"message": "Batch deleted"}, status=204)
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

class GeneratePDFView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, batch_id):
        try:
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Page 1: Header and Stats
            p.setFont("Helvetica-Bold", 20)
            p.drawString(50, height - 50, f"Chemical Equipment Report")
            
            p.setFont("Helvetica", 12)
            p.drawString(50, height - 75, f"Dataset: {batch.filename}")
            p.drawString(50, height - 95, f"Generated: {batch.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Draw Stats
            p.setFont("Helvetica-Bold", 14)
            p.drawString(50, height - 130, "Summary Statistics")
            
            stats = batch.equipment.aggregate(
                avg_flow=Avg('flowrate'), 
                avg_press=Avg('pressure'),
                avg_temp=Avg('temperature'),
                count=Count('id')
            )
            
            p.setFont("Helvetica", 11)
            y = height - 160
            p.drawString(70, y, f"Total Equipment Units: {stats['count']}")
            p.drawString(70, y-20, f"Average Flowrate: {stats['avg_flow']:.2f} m³/hr")
            p.drawString(70, y-40, f"Average Pressure: {stats['avg_press']:.2f} bar")
            p.drawString(70, y-60, f"Average Temperature: {stats['avg_temp']:.2f} °C")
            
            # Generate Type Distribution Chart
            data_items = batch.equipment.all()
            type_counts = {}
            for item in data_items:
                t = item.equipment_type
                type_counts[t] = type_counts.get(t, 0) + 1
            
            # Create bar chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Bar chart
            types = list(type_counts.keys())
            counts = list(type_counts.values())
            ax1.bar(types, counts, color='steelblue')
            ax1.set_xlabel('Equipment Type')
            ax1.set_ylabel('Count')
            ax1.set_title('Equipment Distribution')
            ax1.tick_params(axis='x', rotation=45)
            
            # Pie chart
            ax2.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Type Distribution')
            
            plt.tight_layout()
            
            # Save chart to buffer
            chart_buffer = io.BytesIO()
            plt.savefig(chart_buffer, format='png', dpi=150, bbox_inches='tight')
            chart_buffer.seek(0)
            plt.close()
            
            # Add chart to PDF
            img = ImageReader(chart_buffer)
            p.drawImage(img, 50, height - 500, width=500, height=200, preserveAspectRatio=True)
            
            # Equipment Data Table
            p.setFont("Helvetica-Bold", 12)
            p.drawString(50, height - 530, "Equipment Details")
            
            y = height - 560
            p.setFont("Helvetica-Bold", 9)
            p.drawString(50, y, "Name")
            p.drawString(180, y, "Type")
            p.drawString(280, y, "Flow")
            p.drawString(340, y, "Press")
            p.drawString(400, y, "Temp")
            
            # Draw data rows
            y -= 20
            p.setFont("Helvetica", 8)
            for item in data_items[:15]:  # First 15 items
                if y < 50:  # New page if needed
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica-Bold", 9)
                    p.drawString(50, y, "Name")
                    p.drawString(180, y, "Type")
                    p.drawString(280, y, "Flow")
                    p.drawString(340, y, "Press")
                    p.drawString(400, y, "Temp")
                    y -= 20
                    p.setFont("Helvetica", 8)
                
                p.drawString(50, y, str(item.equipment_name)[:20])
                p.drawString(180, y, str(item.equipment_type)[:15])
                p.drawString(280, y, f"{item.flowrate:.1f}")
                p.drawString(340, y, f"{item.pressure:.1f}")
                p.drawString(400, y, f"{item.temperature:.1f}")
                y -= 15
            
            # Footer
            p.setFont("Helvetica", 8)
            p.drawString(50, 30, "Generated by ChemViz - FOSSEE Project")
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=f"report_{batch.filename.replace('.csv', '')}.pdf")
            
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)