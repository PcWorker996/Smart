"""Run this once to generate multipage.pdf test fixture"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_multipage_pdf():
    c = canvas.Canvas("multipage.pdf", pagesize=letter)
    
    # Page 1
    c.drawString(100, 700, "Page 1: Introduction")
    c.drawString(100, 680, "This is the first page of the document.")
    c.showPage()
    
    # Page 2
    c.drawString(100, 700, "Page 2: Content")
    c.drawString(100, 680, "This is the second page with more content.")
    c.showPage()
    
    # Page 3
    c.drawString(100, 700, "Page 3: Conclusion")
    c.drawString(100, 680, "This is the final page of the document.")
    c.showPage()
    
    c.save()
    print("Created multipage.pdf")

if __name__ == "__main__":
    create_multipage_pdf()
