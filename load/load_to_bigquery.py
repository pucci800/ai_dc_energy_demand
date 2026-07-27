import os
from pathlib import Path

import pandas as pd
from google.cloud import bigquery


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "data" / "ai_energy_clean.csv"


def get_required_env_variable(name: str) -> str:
    """
    Return a required environment variable.

    Raises:
        ValueError: If the variable is missing or empty.
    """
    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}"
        )

    return value


def load_clean_data(file_path: Path) -> pd.DataFrame:
    """
    Load and validate the processed CSV file.
    """
    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed data file was not found: {file_path}\n"
            "Run the extract and transform steps before loading to BigQuery."
        )

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        raise ValueError(
            f"The processed data file is empty: {file_path}"
        )

    if "year" not in dataframe.columns:
        raise ValueError(
            "Required column 'year' is missing from the processed dataset."
        )

    dataframe = dataframe.drop_duplicates(subset=["year"])

    return dataframe


def load_to_bigquery() -> None:
    """
    Load the processed energy-demand dataset into BigQuery.
    """
    project_id = get_required_env_variable("GCP_PROJECT_ID")
    dataset_id = get_required_env_variable("BQ_DATASET_ID")
    table_name = os.getenv(
        "BQ_TABLE_NAME",
        "ai_us_energy_clean",
    )

    table_id = f"{project_id}.{dataset_id}.{table_name}"

    dataframe = load_clean_data(DATA_FILE)

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(
        f"[LOAD START] Loading {len(dataframe)} rows "
        f"into BigQuery table: {table_id}"
    )

    load_job = client.load_table_from_dataframe(
        dataframe,
        table_id,
        job_config=job_config,
    )

    load_job.result()

    destination_table = client.get_table(table_id)

    print(
        f"[LOAD SUCCESS] Loaded "
        f"{destination_table.num_rows} rows "
        f"into BigQuery table: {table_id}"
    )


if __name__ == "__main__":
    try:
        load_to_bigquery()
    except Exception as error:
        print(f"[LOAD ERROR] {error}")
        raise
