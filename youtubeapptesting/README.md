# youtubeapptesting Directory

Contains multiple iterations of a YouTube sentiment analysis web app. Each numbered folder is a different prototype using Flask and various helper scripts.

Common utilities such as `analyze.py` and `keywordyoutube.py` provide core functionality for fetching comments and evaluating sentiment. Check the individual app folders for their own `requirements.txt` files and instructions.

Before running any of the Flask apps, define a `SECRET_KEY` environment variable:

```bash
export SECRET_KEY="your-random-string"
```

Each app reads `SECRET_KEY` from the environment when starting.
