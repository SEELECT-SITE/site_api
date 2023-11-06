# Imports
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image

# Function to generate attendance sheet for an event
def generate_attendance_sheet(participants=[], event=None):
    
    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="attendance_sheet.pdf"'

    # Create the PDF using ReportLab
    document = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Add logo above the header
    logo_path = './utils/static/img/logo.png'  # Provide the actual path to your logo
    logo = Image(logo_path, width=100, height=100)  # Adjust width and height as needed

    elements.append(logo)
    elements.append(Spacer(1, 12))  # Add some space between logo and event info
    
    # Add event information as header
    event_info = [
        (f"Attendance Sheet", "Title"),
        (f"{event.id} - {event.title}", "Heading2"),
        (f"Host: {event.host}", "Heading3"),
        (f"Category: {event.category}",  "Heading3"),
        (f"Inscriptions: {event.number_of_inscriptions} / {event.max_number_of_inscriptions}",  "Heading3"),
    ]
    
    # Get the default styles for paragraphs
    styles = getSampleStyleSheet()
    
    for info in event_info:
        # Define a custom style with Times New Roman font
        style = ParagraphStyle(
            name='TimesNewRoman',
            fontName='Times-Roman',
            parent=styles[info[1]]
        )
        elements.append(Paragraph(info[0], style))
    elements.append(Spacer(1, 12))  # Add some space between event info and table

    # Create a list of lists to represent the table
    data = [["Kit", "Payment", "Name", "Email", "Presence"]]
    
    # Create a custom style for the checkbox
    checkbox_style = ParagraphStyle(
        name='CheckboxStyle',
        fontSize=12,
        leading=14,
        textColor="#FFFFFF",
    )
    
    for participant in participants:
        data.append([participant["kit_model"], participant["kit_status"], participant["name"], participant["email"], Paragraph('&#9744;', style=checkbox_style)])

    # Define the column widths (in points)
    col_widths = [75, 50, 220, 190, 50]

    # Create the table with specified column widths
    table = Table(data, colWidths=col_widths)
    
    # Table style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blueviolet),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10)
    ]))

    # Add the table to the list of elements
    elements.append(table)

    # Build the PDF
    document.build(elements)
        
    return response