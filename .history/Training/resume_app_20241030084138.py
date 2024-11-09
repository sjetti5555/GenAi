from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def resume():
    # HTML & CSS Template mimicking Netflix main page styling
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume - [Your Name]</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background-color: #141414;
                color: #ffffff;
                text-align: center;
            }
            .header {
                background-color: #e50914;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
            }
            .content {
                padding: 40px;
            }
            .section {
                margin: 20px 0;
                padding: 20px;
                background: #333;
                border-radius: 8px;
            }
            h1, h2, h3 {
                margin: 10px;
                color: #e50914;
            }
            p, li {
                color: #b3b3b3;
                font-size: 16px;
            }
            .footer {
                background-color: #333;
                padding: 10px;
                font-size: 14px;
                color: #b3b3b3;
            }
            a {
                color: #e50914;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="header">[Your Name]</div>
        
        <div class="content">
            <div class="section">
                <h2>Objective</h2>
                <p>Data-driven Data Scientist seeking to leverage skills at Netflix to drive insights and optimize user experience.</p>
            </div>
            
            <div class="section">
                <h2>Technical Skills</h2>
                <ul>
                    <li><strong>Programming Languages:</strong> Python, R, SQL, JavaScript</li>
                    <li><strong>Machine Learning & Modeling:</strong> Regression Analysis, Bayesian Inference, Time-Series Forecasting, NLP</li>
                </ul>
            </div>
            
            <div class="section">
                <h2>Professional Experience</h2>
                <p>[Job Title] - [Company Name]</p>
                <p>Briefly describe key accomplishments, highlighting data-driven achievements relevant to Netflix's needs.</p>
            </div>
            
            <div class="section">
                <h2>Education</h2>
                <p>[Degree] in [Field] from [University Name]</p>
            </div>
            
            <div class="section">
                <h2>Contact</h2>
                <p>Email: [Your Email]</p>
                <p>LinkedIn: <a href="[LinkedIn URL]">LinkedIn Profile</a></p>
            </div>
        </div>
        
        <div class="footer">
            &copy; [Current Year] - [Your Name]. All rights reserved.
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
