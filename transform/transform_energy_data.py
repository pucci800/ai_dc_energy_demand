import pandas as pd
from pathlib import Path

# Define file paths
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
input_file = DATA_DIR / "ai_energy_raw.csv"
output_file = DATA_DIR / "ai_energy_clean.csv"

# Load data
df = pd.read_csv(input_file)

# Transformations
df['YoY_growth_pct'] = df['total_energy_TWh'].pct_change () * 100
df['rolling_3yr_avg'] = df['total_energy_TWh'].rolling(window=3).mean()

# Round for readability
df = df.round(2)

# Save transformed data
df.to_csv(output_file, index=False)
print(f"[TRANSFORM SUCCESS] Clean data saved to: {output_file}")
