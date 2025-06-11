# GenAi Project

This repository contains various scripts and applications. Some of the YouTube sentiment analysis apps require a YouTube Data API key. Provide this key through the `YOUTUBE_API_KEY` environment variable before running any of the applications.


## Updating YouTube Apps

The key previously stored in `youtubeapptesting/1youtubeapp/requirements.txt` has been removed. Set the `YOUTUBE_API_KEY` environment variable before running any scripts in `youtubeapptesting/1youtubeapp`.

## Environment Setup

Before running any of the YouTube sentiment analysis apps, export your YouTube Data API key:

```bash
export YOUTUBE_API_KEY=your_key_here
```

This key will be read automatically by the apps via the `YOUTUBE_API_KEY` environment variable.
