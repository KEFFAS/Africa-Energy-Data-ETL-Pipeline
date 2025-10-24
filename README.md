# 🌍 Africa Energy Data Pipeline

This project automates the extraction, transformation, and loading (ETL) of energy-related data from the **Africa Energy Portal** into **MongoDB Atlas**.  
It converts messy, unstructured data into a clean, analysis-ready dataset for easier visualization and reporting.

---

## 🚀 Overview

The **Africa Energy Data Pipeline** automates the collection and transformation of energy indicators across African countries from the [Africa Energy Portal](https://africa-energy-portal.org/).  
The script extracts data dynamically (handling JavaScript-rendered pages), reshapes it from long to wide format, and stores it in a **MongoDB Atlas** collection for easy querying and analysis.

## ⚙️ Pipeline Workflow

1. **Extract** – Fetches energy data from the Africa Energy Portal.
2. **Transform** – Cleans, normalizes, and reshapes the dataset into wide format (years 2000–2024).
3. **Load** – Inserts the transformed dataset into a MongoDB Atlas collection.
4. **Verify** – Confirms the data shape, structure, and successful upload.

---

## 🧠 Technologies Used

| Component | Technology |
|------------|-------------|
| Language | Python 3 |
| Data Handling | pandas |
| Database | MongoDB Atlas |
| HTTP Requests | requests / cloudscraper |
| BSON Serialization | bson |
| Environment Management | python-dotenv |
| Notebook Conversion | nbconvert |

---

## 📁 Project Structure
The repository is organized as follows:
``bash
Africa-Energy-Data-ETL-Pipeline/
├── africa_energy_etl.py          
├── requirements.txt             
├── .gitignore                    
└── README.md
       

## 🧩 Setup Instructions

## Clone the Repository

``bash
git clone https://github.com/yourusername/Africa-Energy-Data-ETL-Pipeline.git
cd Africa-Energy-Data-ETL-Pipeline

## Create and Activate a Virtual Environment

It’s recommended to use a virtual environment to manage project dependencies.

### 🪟 On Windows:
``bash
python -m venv venv
venv\Scripts\activate

## 🧾 Output Format

### After running the pipeline, you should see logs in your terminal similar to:
``bash
- Status: 200
- Content-Type: application/json
- Length: 12976099
- Records returned: 34
- Unique countries found: 54
- ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros', 'Congo Democratic Republic', 'Congo Republic', "Cote d'Ivoire", 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe']



### The MongoDB collection (`energydata`) will contain documents in the following structure:

``json
{
  "country": "Kenya",
  "country_serial": 404,
  "metric": "Electricity generation, Total (GWh)",
  "unit": "GWh",
  "sector": "Electricity",
  "sub_sector": "Supply",
  "sub_sub_sector": "Total generation",
  "source_link": "https://africa-energy-portal.org/data",
  "source": "Africa Energy Portal",
  "2000": 5460.2,
  "2001": 5532.1,
  "2002": 5600.8,
  ...
  "2022": 7850.4
}
``
# 🤝 Contributing

Contributions are welcome!
Feel free to open issues, fork the repo, and submit pull requests to enhance the pipeline or add new data sources.

# 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute with attribution.

# ✉️ Contact

Author: Keffas Nyamu
📧 Email[keffasmutethia@gmail.com]
🌍 GitHub: https://github.com/KEFFAS
