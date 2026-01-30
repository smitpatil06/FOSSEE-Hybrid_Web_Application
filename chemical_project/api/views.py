from django.http import FileResponse
from reportlab.pdfgen import canvas
import io

class GeneratePDFView(APIView):
    def get(self, request, batch_id):
        try:
            batch = UploadBatch.objects.get(id=batch_id)
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            
            # Draw Header
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 800, f"Equipment Report: {batch.filename}")
            
            # Draw Stats
            p.setFont("Helvetica", 12)
            y = 750
            stats = batch.equipment.aggregate(
                avg_flow=Avg('flowrate'), 
                avg_press=Avg('pressure'),
                count=Count('id')
            )
            
            p.drawString(100, y, f"Total Equipment: {stats['count']}")
            p.drawString(100, y-20, f"Average Flowrate: {stats['avg_flow']:.2f}")
            p.drawString(100, y-40, f"Average Pressure: {stats['avg_press']:.2f}")
            
            # Draw Table Header
            y = 650
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, "Name")
            p.drawString(200, y, "Type")
            p.drawString(350, y, "Flowrate")
            p.drawString(450, y, "Pressure")
            
            # Draw Rows (First 20 only to keep it simple)
            y -= 20
            p.setFont("Helvetica", 10)
            for item in batch.equipment.all()[:20]:
                p.drawString(50, y, str(item.equipment_name))
                p.drawString(200, y, str(item.equipment_type))
                p.drawString(350, y, str(item.flowrate))
                p.drawString(450, y, str(item.pressure))
                y -= 15
                if y < 50: break # Stop if page end
                
            p.showPage()
            p.save()
            
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=f"report_{batch.id}.pdf")
            
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)