from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(comments, filename='output.pdf'):
    c = canvas.Canvas(filename, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    for author, comment, timestamp, sentiment, score in comments:
        text.textLine(f"Timestamp: {timestamp}, Author: {author}, Comment: {comment}, Sentiment: {sentiment}, Score: {score}")
    c.drawText(text)
    c.save()
    return filename
