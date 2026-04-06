import os
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'FleetPro - Application Report', border=False, align='C')
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def export_table_to_pdf(title, columns, data, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.pdf"
        
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, title, ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 10)
    col_widths = [190 / len(columns)] * len(columns)
    
    for i, col in enumerate(columns):
        pdf.cell(col_widths[i], 10, str(col), border=1)
    pdf.ln()
    
    pdf.set_font("helvetica", "", 10)
    for row in data:
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 10, str(item), border=1)
        pdf.ln()
        
    out_path = os.path.join(os.path.dirname(__file__), '..', filename)
    pdf.output(out_path)
    return out_path
