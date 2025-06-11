# youtubeapptesting Directory

Contains multiple iterations of a YouTube sentiment analysis web app. Each numbered folder is a different prototype using Flask and various helper scripts.

Common utilities such as `analyze.py` and `keywordyoutube.py` provide core functionality for fetching comments and evaluating sentiment. Check the individual app folders for their own `requirements.txt` files and instructions.

## Database setup

The `4youtubeapp` example uses SQLite. The repository no longer includes the
`database.db` file. When deploying the app, run `python app.py` once (or start
the Docker container) and the application will create the database
automatically. This ensures a fresh database is generated for each deployment.
