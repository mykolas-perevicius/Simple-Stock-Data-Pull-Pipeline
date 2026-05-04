import pandas as pd
from yahooquery import Ticker
from tqdm import tqdm
import time

# ----------------------------
# CONFIG
# ----------------------------
BATCH_SIZE = 200   # Yahoo performs better in chunks
OUTPUT_FILE = "stocks.parquet"  # fast + compact


# ----------------------------
# LOAD TICKERS
# ----------------------------
def load_tickers():
    # Option 1: from CSV
    # return pd.read_csv("tickers.csv")["symbol"].tolist()

    # Example fallback
    return ["AAPL", "MSFT", "GOOG", "AMZN", "META"]


# ----------------------------
# FETCH DATA
# ----------------------------
def fetch_batch(tickers):
    try:
        t = Ticker(tickers, asynchronous=True)

        income = t.income_statement(frequency='a')
        profiles = t.asset_profile

        return income, profiles
    except Exception as e:
        print(f"Batch error: {e}")
        return None, None


# ----------------------------
# PROCESS DATA
# ----------------------------
def process_data(income, profiles):
    if income is None or len(income) == 0:
        return pd.DataFrame()

    df = income.reset_index()

    # ---------------------------
    # Revenue normalization
    # ---------------------------
    revenue_col = None
    for col in ["TotalRevenue", "totalRevenue", "OperatingRevenue"]:
        if col in df.columns:
            revenue_col = col
            break

    df["revenue"] = df[revenue_col] if revenue_col else None

    if "asOfDate" in df.columns:
        df = df.sort_values("asOfDate")
        df = df.groupby("symbol").tail(1)

    df = df[["symbol", "asOfDate", "revenue"]]

    # ---------------------------
    # FIXED PROFILE HANDLING
    # ---------------------------
    prof_df = pd.DataFrame.from_dict(profiles, orient="index").reset_index()

    prof_df = prof_df.rename(columns={"index": "symbol"})

    # pick only what we care about (safe subset)
    keep = [c for c in ["symbol", "sector", "industry"] if c in prof_df.columns]
    prof_df = prof_df[keep]

    # ---------------------------
    # MERGE
    # ---------------------------
    return df.merge(prof_df, on="symbol", how="left")

# ----------------------------
# MAIN PIPELINE
# ----------------------------
def run_pipeline(tickers):
    results = []

    for i in tqdm(range(0, len(tickers), BATCH_SIZE)):
        batch = tickers[i:i+BATCH_SIZE]

        income, profiles = fetch_batch(batch)
        df = process_data(income, profiles)

        if not df.empty:
            results.append(df)

        time.sleep(1)  # be polite

    final_df = pd.concat(results, ignore_index=True)

    return final_df


# ----------------------------
# ENTRYPOINT
# ----------------------------
if __name__ == "__main__":
    tickers = load_tickers()

    print(f"Processing {len(tickers)} tickers...")

    df = run_pipeline(tickers)

    print(df.head())

    OUTPUT_FILE = "stocks.csv"
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved to {OUTPUT_FILE}")