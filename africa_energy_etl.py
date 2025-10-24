# Africa Energy Data Extraction & Mongo Load

# importing libraries
import os
import json
import pandas as pd
import cloudscraper
from pymongo import MongoClient
from bson import SON
from dotenv import load_dotenv


def fetch_energy_data():
    """Fetches data from Africa Energy Portal via POST request."""
    url = "https://africa-energy-portal.org/get-database-data"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/141.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://africa-energy-portal.org",
        "Referer": "https://africa-energy-portal.org/database",
    }

    payload = {
        "mainGroup": "Electricity",
        "mainIndicator[]": ["Access", "Supply", "Technical"],
        "mainIndicatorValue[]": [
            "Population access to electricity-National (% of population)",
            "Population access to electricity-Rural (% of population)",
            "Population access to electricity-Urban (% of population)",
            "Population with access to electricity-National (millions of people)",
            "Population with access to electricity-Rural (millions of people)",
            "Population with access to electricity-Urban (millions of people)",
            "Population without access to electricity-National (millions of people)",
            "Population without access to electricity-Rural (millions of people)",
            "Population without access to electricity-Urban (millions of people)",
            "Electricity export (GWh)",
            "Electricity final consumption (GWh)",
            "Electricity final consumption per capita (KWh)",
            "Electricity generated from biofuels and waste (GWh)",
            "Electricity generated from fossil fuels (GWh)",
            "Electricity generated from geothermal energy (GWh)",
            "Electricity generated from hydropower (GWh)",
            "Electricity generated from nuclear power (GWh)",
            "Electricity generated from renewable sources (GWh)",
            "Electricity generated from solar, wind, tide, wave and other sources (GWh)",
            "Electricity generation per capita (KWh)",
            "Electricity generation, Total (GWh)",
            "Electricity import (GWh)",
            "Electricity: Net imports ( GWh )",
            "Electricity installed capacity in Bioenergy (MW)",
            "Electricity installed capacity in Fossil fuels (MW)",
            "Electricity installed capacity in Geothermal (MW)",
            "Electricity installed capacity in Hydropower (MW)",
            "Electricity installed capacity in Non-renewable energy (MW)",
            "Electricity installed capacity in Nuclear (MW)",
            "Electricity installed capacity in Solar (MW)",
            "Electricity installed capacity in Total renewable energy (MW)",
            "Electricity installed capacity in Wind (MW)",
            "Electricity installed capacity in other Non-renewable energy (MW)",
            "Electricity installed capacity, Total (MW)",
        ],
        "year[]": list(range(2000, 2023)),
        "name[]": [
            "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
            "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros",
            "Congo Democratic Republic", "Congo Republic", "Cote d'Ivoire", "Djibouti",
            "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon",
            "Gambia", "Ghana", "Guinea", "Guinea Bissau", "Kenya", "Lesotho", "Liberia",
            "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
            "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
            "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
            "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe",
        ],
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=headers, data=payload)

    print(f"📡 Fetch Status: {response.status_code}")
    print(f"Content Length: {len(response.text)} bytes")

    try:
        data = response.json()
    except Exception as e:
        print(" Error decoding JSON:", e)
        print(response.text[:500])
        data = []

    print(f" Records returned: {len(data)}")
    return data


def transform_data(raw_data):
    """Transforms nested JSON to wide-format DataFrame."""
    rows = []
    for metric_block in raw_data:
        metric_name = metric_block.get("_id")
        for record in metric_block.get("data", []):
            rows.append({
                "country": record.get("name"),
                "country_serial": record.get("id"),
                "metric": metric_name,
                "unit": record.get("unit"),
                "sector": record.get("indicator_group"),
                "sub_sector": record.get("indicator_topic"),
                "sub_sub_sector": record.get("indicator_name"),
                "source_link": "https://africa-energy-portal.org" + record.get("url", ""),
                "source": record.get("indicator_source"),
                "year": record.get("year"),
                "value": record.get("score"),
            })

    df_long = pd.DataFrame(rows)
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

    # Pivot into wide format
    df_wide = df_long.pivot_table(
        index=["country", "country_serial", "metric", "unit",
               "sector", "sub_sector", "sub_sub_sector",
               "source_link", "source"],
        columns="year",
        values="value",
        aggfunc="first"
    ).reset_index()

    # Ensure all years (2000–2022) exist
    all_years = [str(y) for y in range(2000, 2023)]
    df_wide.columns = df_wide.columns.map(str)
    for y in all_years:
        if y not in df_wide.columns:
            df_wide[y] = None

    # Reorder columns
    base_cols = ["country", "country_serial", "metric", "unit",
                 "sector", "sub_sector", "sub_sub_sector",
                 "source_link", "source"]
    df_wide = df_wide[base_cols + all_years]

    print(f"Final dataset shape: {df_wide.shape}")
    return df_wide


def save_to_mongo(df):
    """Inserts final DataFrame into MongoDB (Atlas/local)."""
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI not found. Please check your .env file.")

    client = MongoClient(mongo_uri)
    db = client["energydb"]
    collection = db["energydata"]

    collection.delete_many({})
    records = [SON([(col, row[col]) for col in df.columns]) for _, row in df.iterrows()]
    collection.insert_many(records)

    print(f" Inserted {len(records)} documents into MongoDB successfully.")


def main():
    """Main ETL pipeline runner."""
    print(" Starting Africa Energy Data Extraction Pipeline...")
    raw_data = fetch_energy_data()

    if not raw_data:
        print(" No data retrieved. Exiting.")
        return

    print(" Transforming data...")
    df_wide = transform_data(raw_data)

    print(" Saving data to MongoDB...")
    save_to_mongo(df_wide)

    print("Pipeline completed successfully!")


# Run script
if __name__ == "__main__":
    main()
