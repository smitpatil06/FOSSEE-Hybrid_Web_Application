import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from django.http import FileResponse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from .models import UploadBatch, EquipmentData
from .serializers import UploadBatchSerializer, EquipmentDataSerializer


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        try:
            df = pd.read_csv(file_obj)
            required_columns = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
            if not all(col in df.columns for col in required_columns):
                return Response({"error": f"Missing columns. Required: {required_columns}"}, status=400)
        except Exception as e:
            return Response({"error": f"CSV Parse Error: {str(e)}"}, status=400)

        batches = UploadBatch.objects.filter(uploaded_by=request.user).order_by("uploaded_at")
        if batches.count() >= 5:
            batches.first().delete()

        batch = UploadBatch.objects.create(filename=file_obj.name, uploaded_by=request.user)

        equipment_list = [
            EquipmentData(
                batch=batch,
                equipment_name=row["Equipment Name"],
                equipment_type=row["Type"],
                flowrate=row["Flowrate"],
                pressure=row["Pressure"],
                temperature=row["Temperature"],
            )
            for _, row in df.iterrows()
        ]
        EquipmentData.objects.bulk_create(equipment_list)

        return Response({"message": "Success", "batch_id": batch.id}, status=201)


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        batches = UploadBatch.objects.filter(uploaded_by=request.user).order_by("-uploaded_at")
        serializer = UploadBatchSerializer(batches, many=True)
        return Response(serializer.data)


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        try:
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            data = batch.equipment.all()

            stats = data.aggregate(
                avg_flow=Avg("flowrate"),
                avg_press=Avg("pressure"),
                total_count=Count("id"),
            )

            type_counts = {}
            for item in data:
                t = item.equipment_type
                type_counts[t] = type_counts.get(t, 0) + 1

            return Response(
                {
                    "id": batch.id,
                    "filename": batch.filename,
                    "summary": stats,
                    "type_distribution": type_counts,
                    "data": EquipmentDataSerializer(data, many=True).data,
                }
            )
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

    def delete(self, request, batch_id):
        try:
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            batch.delete()
            return Response({"message": "Batch deleted"}, status=204)
        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)


class GeneratePDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):
        return self.post(request, batch_id)

    def post(self, request, batch_id):
        try:
            batch = UploadBatch.objects.get(id=batch_id, uploaded_by=request.user)
            chart_config = request.data.get("chart_config", []) if request.data else []
            if not isinstance(chart_config, list):
                return Response({"error": "chart_config must be a list"}, status=400)

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                leftMargin=40,
                rightMargin=40,
                topMargin=80,
                bottomMargin=50,
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "TitleStyle",
                parent=styles["Heading2"],
                fontSize=16,
                textColor=colors.HexColor("#0f172a"),
                spaceAfter=8,
            )
            body_style = ParagraphStyle(
                "BodyStyle",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.HexColor("#0f172a"),
            )

            stats = batch.equipment.aggregate(
                avg_flow=Avg("flowrate"),
                avg_press=Avg("pressure"),
                avg_temp=Avg("temperature"),
                count=Count("id"),
            )

            elements = []
            elements.append(Paragraph("ChemViz Analytics Report", title_style))
            elements.append(Paragraph(f"<b>File Name:</b> {batch.filename}", body_style))
            elements.append(Paragraph(f"<b>Batch ID:</b> {batch.id}", body_style))
            elements.append(Spacer(1, 10))

            summary_data = [
                ["Total Equipment Count", "Average Flowrate", "Average Pressure"],
                [
                    str(stats["count"]),
                    f"{stats['avg_flow']:.2f} m³/hr" if stats["avg_flow"] else "-",
                    f"{stats['avg_press']:.2f} bar" if stats["avg_press"] else "-",
                ],
            ]
            summary_table = Table(summary_data, colWidths=[160, 160, 160])
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5f5")),
                    ]
                )
            )
            elements.append(summary_table)
            elements.append(Spacer(1, 16))

            data_items = list(batch.equipment.all())
            type_counts = {}
            flowrates = []
            pressures = []
            temperatures = []
            for item in data_items:
                t = item.equipment_type
                type_counts[t] = type_counts.get(t, 0) + 1
                flowrates.append(item.flowrate)
                pressures.append(item.pressure)
                temperatures.append(item.temperature)

            if chart_config and data_items:
                elements.append(Paragraph("Charts Overview", title_style))

                def create_chart_image(chart_type, metric, title, color):
                    categorical_metrics = {"type_distribution"}
                    continuous_metrics = {"flowrate", "pressure", "temperature"}
                    scatter_metrics = {
                        "flowrate_vs_pressure",
                        "flowrate_vs_temperature",
                        "pressure_vs_temperature",
                    }

                    def error_image(message):
                        fig, ax = plt.subplots(figsize=(3.2, 2.3), dpi=140)
                        ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=9)
                        ax.axis("off")
                        fig.tight_layout()
                        buf = io.BytesIO()
                        fig.savefig(buf, format="png", dpi=140)
                        plt.close(fig)
                        buf.seek(0)
                        return Image(buf, width=240, height=160)

                    fig, ax = plt.subplots(figsize=(3.2, 2.3), dpi=140)

                    if metric == "type_distribution":
                        labels = list(type_counts.keys())
                        values = list(type_counts.values())
                    elif metric == "flowrate":
                        labels = [f"U{i+1}" for i in range(len(flowrates))]
                        values = flowrates
                    elif metric == "pressure":
                        labels = [f"U{i+1}" for i in range(len(pressures))]
                        values = pressures
                    elif metric == "temperature":
                        labels = [f"U{i+1}" for i in range(len(temperatures))]
                        values = temperatures
                    elif metric in [
                        "flowrate_vs_pressure",
                        "flowrate_vs_temperature",
                        "pressure_vs_temperature",
                    ]:
                        labels = []
                        values = []
                    else:
                        labels = []
                        values = []

                    if chart_type in ["pie", "doughnut", "radar", "polar"] and metric not in categorical_metrics:
                        plt.close(fig)
                        return error_image("Invalid data for categorical chart")

                    if chart_type in ["line", "area"] and metric not in continuous_metrics:
                        plt.close(fig)
                        return error_image("Invalid data for Line/Area")

                    if chart_type == "scatter" and metric not in scatter_metrics:
                        plt.close(fig)
                        return error_image("Invalid data for Scatter")

                    if chart_type == "radar":
                        if not labels:
                            plt.close(fig)
                            return error_image("No data for Radar")
                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False).tolist()
                        values = values + [values[0]]
                        angles = angles + [angles[0]]
                        ax = fig.add_subplot(111, polar=True)
                        ax.plot(angles, values, color=color or "#3b82f6", linewidth=2)
                        ax.fill(angles, values, color=color or "#93c5fd", alpha=0.3)
                        ax.set_xticks(angles[:-1])
                        ax.set_xticklabels(labels, fontsize=6)
                    elif chart_type == "polar":
                        if not labels:
                            plt.close(fig)
                            return error_image("No data for Polar")
                        ax = fig.add_subplot(111, polar=True)
                        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False)
                        ax.bar(angles, values, color=color or "#3b82f6", alpha=0.8, width=0.6)
                        ax.set_xticks(angles)
                        ax.set_xticklabels(labels, fontsize=6)
                    elif chart_type == "bar":
                        ax.bar(labels, values, color=color or "#3b82f6", alpha=0.85)
                        ax.tick_params(axis="x", rotation=30, labelsize=6)
                    elif chart_type == "line":
                        ax.plot(values, color=color or "#3b82f6", linewidth=2)
                    elif chart_type == "area":
                        ax.plot(values, color=color or "#3b82f6", linewidth=2)
                        ax.fill_between(range(len(values)), values, color=color or "#93c5fd", alpha=0.4)
                    elif chart_type == "pie":
                        pie_colors = [color] if color not in ["multi", None] else None
                        ax.pie(values, labels=labels, autopct="%1.0f%%", textprops={"fontsize": 6}, colors=pie_colors)
                    elif chart_type == "doughnut":
                        pie_colors = [color] if color not in ["multi", None] else None
                        ax.pie(values, labels=labels, autopct="%1.0f%%", textprops={"fontsize": 6}, colors=pie_colors)
                        centre_circle = plt.Circle((0, 0), 0.55, fc="white")
                        ax.add_artist(centre_circle)
                    elif chart_type == "scatter":
                        if metric == "flowrate_vs_temperature":
                            x_vals, y_vals = flowrates, temperatures
                        elif metric == "pressure_vs_temperature":
                            x_vals, y_vals = pressures, temperatures
                        else:
                            x_vals, y_vals = flowrates, pressures
                        ax.scatter(x_vals, y_vals, color=color or "#10b981", alpha=0.7, s=12)
                    else:
                        ax.bar(labels, values, color=color or "#3b82f6", alpha=0.85)

                    ax.set_title(title, fontsize=8)
                    fig.tight_layout()
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", dpi=140)
                    plt.close(fig)
                    buf.seek(0)
                    return Image(buf, width=240, height=160)

                chart_images = []
                for cfg in chart_config:
                    chart_type = str(cfg.get("type", "bar")).lower()
                    metric = str(cfg.get("metric", "type_distribution")).lower()
                    title = str(cfg.get("title", "Chart"))
                    color = cfg.get("color")
                    chart_images.append(create_chart_image(chart_type, metric, title, color))

                cols = 2
                rows = []
                for i in range(0, len(chart_images), cols):
                    row = chart_images[i:i + cols]
                    if len(row) < cols:
                        row.append(Spacer(1, 1))
                    rows.append(row)

                chart_table = Table(rows, colWidths=[250, 250])
                chart_table.setStyle(
                    TableStyle(
                        [
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
                            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                        ]
                    )
                )
                elements.append(chart_table)
                elements.append(Spacer(1, 16))
            else:
                elements.append(Paragraph("Summary Only Report", title_style))
                elements.append(Spacer(1, 8))

            table_data = [["Name", "Type", "Flowrate", "Pressure", "Temperature"]]
            for item in data_items:
                table_data.append(
                    [
                        str(item.equipment_name),
                        str(item.equipment_type),
                        f"{item.flowrate:.2f}",
                        f"{item.pressure:.2f}",
                        f"{item.temperature:.2f}",
                    ]
                )

            main_table = Table(table_data, repeatRows=1, colWidths=[160, 110, 90, 90, 90])
            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
            for row in range(1, len(table_data)):
                bg = colors.HexColor("#f8fafc") if row % 2 == 0 else colors.white
                table_style.add("BACKGROUND", (0, row), (-1, row), bg)
            main_table.setStyle(table_style)
            elements.append(main_table)

            report_date = timezone.now().strftime("%Y-%m-%d")

            def draw_header(canvas_obj, doc_obj):
                canvas_obj.saveState()
                canvas_obj.setFont("Helvetica-Bold", 13)
                canvas_obj.setFillColor(colors.HexColor("#0f172a"))
                canvas_obj.drawString(40, letter[1] - 40, "ChemViz Analytics Report")
                canvas_obj.setFont("Helvetica", 9)
                canvas_obj.setFillColor(colors.HexColor("#475569"))
                canvas_obj.drawRightString(letter[0] - 40, letter[1] - 40, report_date)
                canvas_obj.setStrokeColor(colors.HexColor("#cbd5e1"))
                canvas_obj.setLineWidth(1)
                canvas_obj.line(40, letter[1] - 48, letter[0] - 40, letter[1] - 48)
                canvas_obj.restoreState()

            class NumberedCanvas(canvas.Canvas):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._saved_page_states = []

                def showPage(self):
                    self._saved_page_states.append(dict(self.__dict__))
                    super().showPage()

                def save(self):
                    total_pages = len(self._saved_page_states)
                    for state in self._saved_page_states:
                        self.__dict__.update(state)
                        self.setFont("Helvetica", 9)
                        self.setFillColor(colors.HexColor("#64748b"))
                        self.drawRightString(
                            letter[0] - 40,
                            30,
                            f"Page {self._pageNumber} of {total_pages}",
                        )
                        super().showPage()
                    super().save()

            doc.build(
                elements,
                onFirstPage=draw_header,
                onLaterPages=draw_header,
                canvasmaker=NumberedCanvas,
            )

            buffer.seek(0)
            filename = f"report_{batch.filename.replace('.csv', '')}.pdf"
            response = FileResponse(buffer, as_attachment=True, filename=filename, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response

        except UploadBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)
