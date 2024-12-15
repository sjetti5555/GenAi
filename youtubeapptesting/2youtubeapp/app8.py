from flask import Flask, render_template, request, Response, send_file
import sentiment_analysis as sa
from utils.pdf_generation import generate_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        video_id = sa.extract_video_id(video_url)
        if video_id:
            comments = sa.get_video_comments(video_id)
            return render_template('results.html', comments=comments, video_id=video_id)
        else:
            return 'Invalid YouTube URL', 400
    return render_template('index.html')

@app.route('/download-csv/<video_id>')
def download_csv(video_id):
    comments = sa.get_video_comments(video_id)
    csv = sa.create_csv(comments)
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={video_id}_sentiment_analysis.csv"}
    )

@app.route('/download-pdf/<video_id>')
def download_pdf(video_id):
    comments = sa.get_video_comments(video_id)
    pdf_path = generate_pdf(comments, f"{video_id}_analysis.pdf")
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
