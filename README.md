# GenAi Repository

<<<<<<< codex/add-readme.md-files-for-project-and-folders
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

=======
This project hosts assorted experiments, datasets and utilities around data science and generative AI.  The root of the repository contains standalone Python scripts plus larger collections of material in dedicated folders.

## Directory layout

- `*.py` – individual scripts such as `datacsv.py` for web scraping, `train.py` for route visualisation and other small utilities.
- `Recap/` – learning resources split into subfolders (`1Mathematics`, `2Python`, `3DataScience`, etc.) with example code and small data files.
- `Recapupto24102024/` – additional datasets and scripts including an `EV_Dataset.csv` and code under `PresentationData/` for statistical analysis.
- `youtubeapptesting/` – several sample applications that analyse YouTube content.  Each numbered folder contains Flask apps and helper scripts.
- `TrafficDataset.ipynb` – a Jupyter notebook demonstrating traffic data analysis.

## Quickstart

1. **Set up a Python environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirement.txt
   ```
   The file `requirement.txt` lists the basic packages needed (`requests` and `bs4`).  Some folders provide their own `requirements.txt` if additional dependencies are required.

2. **Run an example script**
   ```bash
   python datacsv.py
   ```
   `datacsv.py` prompts for a website URL and depth to crawl, then saves discovered links to CSV and visualises them.

3. **Explore the notebook**
   ```bash
   jupyter notebook TrafficDataset.ipynb
   ```
   Open the notebook in your browser to inspect the analysis steps.

For more specialised demos (e.g. the YouTube apps) refer to the code inside each folder.
>>>>>>> main
