# GenAi Dataset Setup

This repository expects certain datasets and SQLite databases for the example notebooks and scripts. To keep the repository lightweight, these files are stored in the `data/` directory.

## Required files

- `EV_Dataset.csv`
- `Loan_Default.csv`
- `Traffic_Volume.csv`
- `andhra_pradesh_industry_data.db`
- `industrial_policy.db`
- `presentation_andhra_pradesh_industry_data.db`
- `database.db`

## Downloading the datasets

1. Create the `data/` directory in the repository root if it does not exist:
   ```bash
   mkdir -p data
   ```
2. Download each dataset from its source (most are available on Kaggle) and place the files in the `data/` directory using the names above.
3. Once the files are in place, the example scripts will load them from `data/` automatically.

For large files you can also configure [Git LFS](https://git-lfs.github.com/) if you prefer version control of the datasets.
