# AI Data Center Energy Demand ETL Project

This project analyzes U.S. data center electricity demand trends associated with the growth of artificial intelligence (AI) and computing infrastructure.

The project uses a Python-based ETL pipeline to extract source data, transform it into an analysis-ready dataset, and load the processed data into Google BigQuery. Docker provides a reproducible execution environment, while Tableau Public is used to visualize the resulting trends and key performance indicators.

This project was originally built as an end-to-end data engineering portfolio project and later refactored to improve reproducibility, configuration management, security, documentation, and repository organization.

---

## Architecture

```text
Public Data Source
        |
        v
Python Extract
        |
        v
Raw Data
        |
        v
Python Transform
        |
        v
Processed Data
        |
        v
Google BigQuery
        |
        v
Tableau
```

### Pipeline Responsibilities

- **Extract:** Reads the source energy-demand dataset and creates a raw working copy.
- **Transform:** Calculates analytical metrics and prepares a clean dataset for analysis.
- **Load:** Validates and loads the processed dataset into Google BigQuery.
- **Tableau:** Visualizes energy-demand trends and analytical KPIs.

---

## Tech Stack

- Python
- pandas
- Docker
- Google Cloud BigQuery
- Tableau Public
- Git & GitHub
- Bash

---

## Project Structure

```text
ai_dc_energy_demand/
├── data/                  # Source, raw, and processed datasets
├── docs/
│   └── references/        # Source and research documentation
├── extract/
│   └── extract_energy_data.py
├── load/
│   └── load_to_bigquery.py
├── logs/                  # Local pipeline logs
├── screenshots/           # Tableau dashboard images
├── transform/
│   └── transform_energy_data.py
├── .dockerignore
├── .env.example           # Environment configuration template
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

Local credentials, virtual environments, IDE configuration, operating-system metadata, and other machine-specific files are excluded from version control.

---

## ETL Data Flow

The pipeline processes the data through three CSV stages:

```text
data/us_data_center_energy.csv
            |
            v
        Extract
            |
            v
data/ai_energy_raw.csv
            |
            v
       Transform
            |
            v
data/ai_energy_clean.csv
            |
            v
        BigQuery
```

The Docker commands mount the local `data/` directory into the container so that output created by one pipeline stage remains available to subsequent stages.

---

## Tableau Dashboard

[View the interactive AI Data Center Energy Demand dashboard on Tableau Public](https://public.tableau.com/views/AIDataCenterEnergyDemandDashboard/AIEnergyDemand)

The dashboard includes:

- Total energy demand (TWh)
- Year-over-year (YoY) growth
- Three-year rolling averages
- Interactive year filters
- Measure selection

### Key Insights

- **2014 Energy Demand:** 58 TWh
- **2021 Energy Demand:** 130 TWh
- **2028 Projected Demand:** 325 TWh
- **Peak YoY Growth:** 25% in 2024
- Growth declined from approximately **19.2% to 13.6%** between 2022 and 2023.

### Dashboard Preview

#### Dashboard Overview

![Dashboard Overview](screenshots/Tableau1.png)

#### KPI Detail

![KPI Detail](screenshots/Tableau2.png)

---

# Running the Project

## Prerequisites

To reproduce the project, install:

- Git
- Docker

The BigQuery load stage additionally requires:

- A Google Cloud project
- A BigQuery dataset
- Google Cloud credentials with appropriate BigQuery permissions

The Extract and Transform stages can be run without Google Cloud credentials.

---

## 1. Clone the Repository

```bash
git clone https://github.com/pucci800/ai_dc_energy_demand.git
cd ai_dc_energy_demand
```

---

## 2. Build the Docker Image

From the repository root:

```bash
docker build -t ai-dc-energy-demand .
```

Docker installs the Python dependencies defined in `requirements.txt` and packages the project into a reproducible environment.

---

## 3. Run the Extract Stage

The Extract stage reads:

```text
data/us_data_center_energy.csv
```

and creates:

```text
data/ai_energy_raw.csv
```

Run:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  ai-dc-energy-demand \
  python extract/extract_energy_data.py
```

Expected output:

```text
[EXTRACT SUCCESS] File saved to: /app/data/ai_energy_raw.csv
```

The `data/` directory is mounted into the container so that the generated file persists after the temporary container exits.

---

## 4. Run the Transform Stage

The Transform stage reads:

```text
data/ai_energy_raw.csv
```

and creates:

```text
data/ai_energy_clean.csv
```

Run:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  ai-dc-energy-demand \
  python transform/transform_energy_data.py
```

The transformation currently calculates:

- Year-over-year energy-demand growth
- Three-year rolling average energy demand
- Rounded analytical values for readability

Expected output:

```text
[TRANSFORM SUCCESS] Clean data saved to: /app/data/ai_energy_clean.csv
```

---

# BigQuery Configuration

The BigQuery loader uses environment variables instead of hard-coded project configuration.

This allows the project to be reused with different Google Cloud environments without modifying the Python source code.

## 5. Create Local Environment Configuration

The repository contains:

```text
.env.example
```

Copy it:

```bash
cp .env.example .env
```

Update `.env` with your own Google Cloud configuration:

```text
GCP_PROJECT_ID=your-gcp-project-id
BQ_DATASET_ID=your-bigquery-dataset
BQ_TABLE_NAME=ai_us_energy_clean
GOOGLE_APPLICATION_CREDENTIALS=/run/secrets/gcp_credentials.json
```

The real `.env` file is excluded from Git.

---

## Google Cloud Credentials

Google Cloud credentials should remain outside the repository.

**Never commit service-account credentials, API keys, passwords, or other secrets to GitHub.**

The credential file is mounted into the Docker container at runtime and mounted as read-only.

---

## 6. Run the BigQuery Load Stage

Run:

```bash
docker run --rm \
  --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "/path/to/your/service-account-key.json:/run/secrets/gcp_credentials.json:ro" \
  ai-dc-energy-demand \
  python load/load_to_bigquery.py
```

Replace:

```text
/path/to/your/service-account-key.json
```

with the location of your own Google Cloud credential file.

The loader:

1. Reads `data/ai_energy_clean.csv`
2. Validates that the dataset exists and contains data
3. Validates required columns
4. Removes duplicate years
5. Connects to BigQuery
6. Loads the analytical dataset into the configured table

---

# Security and Configuration

The project separates application code, configuration, and credentials.

```text
Application Code
      |
      | reads configuration
      v
Environment Variables
      |
      | references credentials
      v
External Google Cloud Credentials
```

Repository protections include:

- `.gitignore`
- `.dockerignore`
- `.env.example`
- Environment-based BigQuery configuration
- External credential mounting
- Read-only credential access inside Docker

Real `.env` files and credential files are not intended to be committed to Git.

---

# Data Sources

Primary reference material includes:

- Lawrence Berkeley National Laboratory
- Publicly available research and datasets concerning U.S. data center electricity consumption

Supporting source documentation is stored under:

```text
docs/references/
```

---

# Design Decisions

## Why Docker?

Docker provides a consistent Python environment and dependency set, reducing differences between development machines.

It also makes the project easier to reproduce without requiring users to manually configure a Python virtual environment.

## Why BigQuery?

BigQuery provides a scalable analytical data warehouse and aligns with cloud-based data engineering workflows.

## Why Separate Extract, Transform, and Load?

Separating pipeline responsibilities makes each stage easier to understand, debug, modify, and eventually test independently.

## Why Environment Variables?

Environment-specific configuration is separated from application code so that another user can run the pipeline against their own Google Cloud environment without editing the Python source.

## Why Docker Volumes?

Each `docker run --rm` command creates a temporary container.

Mounting:

```text
./data → /app/data
```

allows pipeline outputs to persist on the host machine and remain available to subsequent pipeline stages.

## Why `WRITE_TRUNCATE`?

The current pipeline rebuilds a complete analytical snapshot, so the destination BigQuery table is replaced during each load.

For an incremental production pipeline, append or merge logic could be used instead.

---

# Limitations and Future Improvements

This project demonstrates portfolio-scale ETL engineering rather than a production data platform.

Potential future improvements include:

- Automated unit and integration tests
- Schema validation
- Additional data-quality checks
- Structured logging
- CI/CD
- Workflow orchestration with Apache Airflow
- Incremental data loading
- Cloud-native secret management
- Direct BigQuery-to-Tableau connectivity
- Automated pipeline monitoring

The Tableau dashboard currently uses exported data rather than a live BigQuery connection.

---

# Lessons Learned

Building and later refactoring this project provided hands-on experience with:

- ETL pipeline architecture
- Python data transformation
- pandas
- Docker containerization
- Docker volumes
- BigQuery loading
- Environment-based configuration
- Credential separation
- Git and GitHub workflows
- Git rebasing
- Merge-conflict resolution
- Repository hygiene
- Debugging
- Technical documentation
- Reproducibility

One of the primary lessons from the project was that a working pipeline is only part of engineering. A project should also be understandable, configurable, secure, and reproducible by someone other than its original developer.

---

# License

This project is licensed under the MIT License.
