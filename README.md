# Antimalarial Potency Prediction

This is the source code for running the Gamma regression predictions for predicting the potency values and inhibition percentages of anti-malarial compounds.

## Quick Start

```bash
git clone https://github.com/dinodev24/antimalarial-potency-prediction
cd antimalarial-potency-prediction/
python -m venv .venv/
source .venv/Scripts/activate # Or .venv/bin/activate for Linux or MacOS
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m jupyter notebook
```
(Click prediction.ipynb)

## Project Structure

```
├── chembl.csv        # Raw dataset from Kaggle
├── database.py       # Python code for collecting the ChEMBL descriptors
├── dataset.csv       # Processed and cleaned code
├── prediction.ipynb  # Notebook with further cleaning and training code
├── README.md
├── requirements.txt
└── requirements-dev.txt
```

## References

### Data Sources
- Kaggle dataset: https://www.kaggle.com/datasets/abdullahamjad1234/chembl-drug-effectiveness-prediction
- ChEMBL: https://www.ebi.ac.uk/chembl/

### Tools & Libraries
- Pandas, NumPy, Statsmodels, Matplotlib