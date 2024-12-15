from fpdf import FPDF

# Initialize PDF instance
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Set title and fonts
pdf.set_font("Arial", size=12, style='B')
pdf.cell(200, 10, txt="Sentiment Analysis App - index.html Explanation", ln=True, align='C')

# Set body text font
pdf.set_font("Arial", size=10)

content = """
1. Document Type and Language Declaration:
   - <!DOCTYPE html>: Declares that the document type is HTML5.
   - <html lang="en">: Starts the HTML document and specifies the language as English (en).

2. Meta Tags and Title:
   - <meta charset="UTF-8">: Specifies the character encoding.
   - <meta name="viewport" content="width=device-width, initial-scale=1.0">: Ensures the page is responsive.
   - <title>Sentiment Analysis App</title>: Sets the browser tab's title.

3. Linking Stylesheets:
   - Bootstrap CSS: Adds responsive design features.
   - Custom CSS: Links to your custom styles.
   - Google Fonts: Imports the "Roboto" font for better typography.
...
"""

# Add content to PDF
pdf.multi_cell(0, 10, content)

# Save the PDF
pdf.output("index_explanation.pdf")
