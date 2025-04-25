import sys
import pandas as pd
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from etl.models import Signal

API_URL = "http://api:8000/data/"
TARGET_URL = "postgresql://user:password@target_db:5432/target_db"


def fetch(date: str) -> pd.DataFrame:
    params = {
        "start": f"{date}T00:00:00",
        "end": f"{date}T23:59:59",
        "variables": ["wind_speed", "power"],
    }
    r = httpx.get(API_URL, params=params, timeout=30.0)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    agg = (
        df.resample("10min")
        .agg(["mean", "min", "max", "std"])
        .rename_axis("timestamp")
    )
    agg.columns = [f"{var}_{stat}" for var, stat in agg.columns]
    return agg.reset_index()


def load(df: pd.DataFrame):
    engine = create_engine(TARGET_URL, future=True)
    with Session(engine) as session:
        for _, row in df.iterrows():
            ts = row["timestamp"]
            for col in df.columns[1:]:
                session.add(
                    Signal(
                        name=col,
                        timestamp=ts,
                        signal_id=hash(col) % 1000,
                        value=row[col],
                    )
                )
        session.commit()


def main():
    if len(sys.argv) != 2:
        sys.exit("Uso: python etl_script.py YYYY-MM-DD")
    date = sys.argv[1]
    raw = fetch(date)
    transformed = transform(raw)
    load(transformed)
    print(f"ETL concluído para {date}")


if __name__ == "__main__":
    main()
