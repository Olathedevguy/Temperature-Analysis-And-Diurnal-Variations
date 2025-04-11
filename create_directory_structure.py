import os

# Define folder structure
project_name = "."

folders = [
    f"{project_name}/data/raw",
    f"{project_name}/data/processed",
    f"{project_name}/notebooks",
    f"{project_name}/scripts",
    f"{project_name}/results/plots",
    f"{project_name}/results/tables",
    f"{project_name}/tests",
]

files = {
    f"{project_name}/README.md": "# Temperature Analysis and Diurnal Variations\n\n",
    f"{project_name}/requirements.txt": "pandas\nnumpy\nscipy\nmatplotlib\nseaborn\njupyter\n",
    f"{project_name}/main.py": "# Entry point script\n\nif __name__ == '__main__':\n    print('Run analysis pipeline here')\n",
    f"{project_name}/scripts/__init__.py": "",
    f"{project_name}/scripts/prepare_data.py": "# Script to clean and prepare raw data\n",
    f"{project_name}/scripts/analyze_diurnal.py": "# Script to perform diurnal analysis\n",
    f"{project_name}/scripts/compare_pairs.py": "# Script to compare matched pairs (case-control)\n",
    f"{project_name}/scripts/plot_utils.py": "# Common plotting utilities\n",
    f"{project_name}/notebooks/exploratory_analysis.ipynb": "",  # Empty Jupyter Notebook
    f"{project_name}/tests/test_analysis.py": "# Tests for analysis functions\n",
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"📁 Project structure '{project_name}' created successfully.")
