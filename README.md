# 📊 Stock Financial Data Pipeline

A lightweight Python pipeline that pulls fundamental financial data (revenue, sector, industry) for thousands of stocks using Yahoo Finance via `yahooquery`.

---

## 🚀 Features

- Pulls financial statements for multiple tickers
- Extracts:
  - Revenue
  - Sector
  - Industry
- Batch processing for scalability (5k+ tickers)
- CSV output for easy analysis
- No paid APIs required

---

## 🧰 Tech Stack

- Python 3.9+
- yahooquery (Yahoo Finance data access)
- pandas
- tqdm

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/stock_pipeline.git
cd stock_pipeline

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
````

---

## ▶️ Usage

```bash
python pipeline.py
```

Output:

```
stocks.csv
```

---

## 📊 Output Columns

* symbol
* asOfDate
* revenue
* sector
* industry

---

## ⚠️ Notes

* Data is sourced from Yahoo Finance via `yahooquery`
* Some tickers may have missing revenue or metadata
* Intended for research and analysis purposes