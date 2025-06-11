# GenAi Repository

This repository contains a variety of experiments and utilities around data analysis, machine learning and web scraping. The code ranges from interactive route planners to sentiment analysis for YouTube videos. Most scripts are written in Python and require the packages listed in `requirement.txt`.

## Major directories

- **Recap/** – Categorized recap of topics such as Mathematics, Python, Data Science, Machine Learning and more. Each subfolder includes small scripts or resources for the corresponding subject.
- **Recapupto24102024/** – Collection of scripts and datasets assembled up to October 2024. It includes EV data analysis, probability examples, industrial policy visualizations and supporting materials in `PresentationData/`.
- **youtubeapptesting/** – Prototypes for a YouTube sentiment‑analysis application built with Flask. Multiple versions (`1youtubeapp` through `4youtubeapp`) show iterations of the web app alongside helper scripts.

Other files at the repository root provide examples such as airline route planners (`AllAirlines.py`, `train.py`), scraping utilities (`datacsv.py`, `ScrapeApplicationDetailsSelenium.py`) and domain‑specific notebooks.

## Running the code

1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
2. Execute a script with Python. Many files prompt for user input or create plots, e.g.
   ```bash
   python AllAirlines.py
   ```
   Check each folder's README for specific instructions.

