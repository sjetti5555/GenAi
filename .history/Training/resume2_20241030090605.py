from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def resume():
    # HTML & CSS Template mimicking LinkedIn profile styling
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LinkedIn-Style Resume - [Your Name]</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f3f2ef;
                margin: 0;
                color: #333;
            }
            .header {
                background-color: #0073b1;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .profile {
                text-align: center;
                margin: 20px;
            }
            .profile img {
                border-radius: 50%;
                width: 150px;
                height: 150px;
            }
            .profile h1 {
                font-size: 24px;
                color: #0073b1;
            }
            .content {
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .section {
                margin: 20px 0;
            }
            h2 {
                color: #333;
                font-size: 20px;
                border-bottom: 2px solid #e1dfdd;
                padding-bottom: 5px;
                margin-bottom: 10px;
            }
            p, li {
                color: #555;
                font-size: 16px;
                line-height: 1.6;
            }
            .contact {
                color: #0073b1;
                font-size: 14px;
                text-align: center;
                margin: 20px 0;
            }
            a {
                color: #0073b1;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            [Your Name] - Data Scientist
        </div>
        
        <div class="profile">
            <img src="[Your Profile Image URL]" alt="Profile Picture">
            <h1>[Your Name]</h1>
            <p>Data Scientist with expertise in machine learning, statistical analysis, and data visualization.</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>About Me</h2>
                <p>Passionate Data Scientist with hands-on experience in developing data-driven solutions, optimizing user engagement, and leveraging statistical models to drive strategic decisions.</p>
            </div>
            
            <div class="section">
                <h2>Experience</h2>
                <p><strong>[Job Title]</strong> - [Company Name]</p>
                <p>• Key accomplishments and data-driven achievements relevant to a Data Scientist role at Netflix.</p>
            </div>
            
            <div class="section">
                <h2>Education</h2>
                <p>[Degree] in [Field] - [University Name]</p>
            </div>
            
            <div class="section">
                <h2>Technical Skills</h2>
                <ul>
                    <li><strong>Languages:</strong> Python, R, SQL, JavaScript</li>
                    <li><strong>Data Analysis:</strong> Regression, Bayesian Inference, Clustering, NLP</li>
                    <li><strong>Tools:</strong> Tableau, Power BI, Jupyter Notebooks, Git</li>
                </ul>
            </div>
            
            <div class="contact">
                <p>Contact: <a href="mailto:[Your Email]">[Your Email]</a> | LinkedIn: <a href="[Your LinkedIn URL]">View Profile</a></p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
