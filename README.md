# GenAi Repository

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
