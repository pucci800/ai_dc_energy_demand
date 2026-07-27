import pandas as pd
from pathlib import Path

# define the path to the directory
DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# read in the data from the CSV
csv_file = DATA_DIR / "us_data_center_energy.csv"
df = pd.read_csv(csv_file)

# save a copy as raw extract output
output_file = DATA_DIR / "ai_energy_raw.csv"
df.to_csv(output_file, index=False)

print(f"[EXTRACT SUCCESS] File saved to: {output_file}")


