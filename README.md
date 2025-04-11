# Temperature Analysis and Diurnal Variations

This project analyzes indoor/outdoor temperature data from various structures in a case-control setting. It performs:

- Diurnal variation analysis with 95% confidence intervals
- Matched pair comparisons across intervention/control arms
- Statistical significance (paired t-tests)

## Structure

- `data/`: Raw and processed datasets
- `scripts/`: Core data processing and analysis modules
- `results/`: Plots and tables output
- `notebooks/`: Exploratory analysis and visualization
- `main.py`: Run full pipeline

## Setup

```bash
pip install -r requirements.txt
python main.py
