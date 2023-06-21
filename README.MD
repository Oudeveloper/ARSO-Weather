# ARSO-Weather Data Retrieval and Storage

The ARSO-Weather project retrieves weather data from the website of the Environmental Agency of the Republic of Slovenia (ARSO) and stores it in a MySQL database.

## Setup

The project requires certain Python packages which can be installed using [pip](https://pip.pypa.io/en/stable/), a Python package manager.

To install the necessary packages, run the following command:

```bash
pip install -r requirements.txt
```

## Project Overview

The project comprises of three main components:

### 1. XML Data Retrieval from ARSO

The `xml_downloader.py` script scrapes the names of XML files from ARSO's website and downloads them asynchronously to a 'tmp' directory. Each time the script is run, it deletes the existing 'tmp' directory and its contents before creating a new one.

### 2. Parsing XML Files and Storing Data in MySQL

The `xml_parser.py` script reads the downloaded XML files and writes the data into a MySQL database. For simplicity, the script extracts and stores the following information:
- Temperature
- Humidity
- Wind speed
- Pressure
- Precipitation
- Date and time
- Solar radiation
- Diffuse solar radiation

### 3. ETL (Extract, Transform, Load) Process

The `etl.sh` shell script orchestrates a simple ETL process that fetches data from ARSO and writes it into a MySQL database.

## Usage

Before running the ETL script, a few setup steps are required:

1. **Update Script Path**: Ensure that you update the path to the location where the script is stored. To make the script executable, run:

   ```bash
   chmod +x etl.sh
   ```

2. **MySQL Configuration**: The scripts require access to your MySQL server. update a `credentials.txt` file in the same directory as your scripts and include your MySQL server's details as follows:

   ```ini
   localhost
   yourusername
   yourpassword
   ```

   Make sure to replace `yourusername`, `yourpassword`, and `yourdatabase` with your actual MySQL credentials and database name. This file is used by the scripts to connect to your MySQL server.


3. **Logging**: The scripts generate a log file named `log.txt` in the same directory. This file will contain information about the execution of the scripts, including any errors or exceptions that might occur. Be sure to check this file regularly for any issues.

### Setting up a Crontab

To automate the ETL process, create a crontab that runs the script every hour. Use the following command to open your crontab file:

```bash
crontab -e
```

Then, add the following line to the crontab file, replacing `/path/to/` with the path to your `etl.sh` script:

```bash
0 * * * * /path/to/etl.sh
```

This will schedule the ETL process to run at the start of every hour.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
