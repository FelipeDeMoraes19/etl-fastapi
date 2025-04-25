from fastapi import FastAPI, Query, HTTPException
from sqlalchemy import create_engine, text
import pandas as pd

app = FastAPI(title="Source Data API")

DATABASE_URL = "postgresql://user:password@source_db:5432/source_db"
engine = create_engine(DATABASE_URL)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/data/")
def get_data(
    start: str,
    end: str,
    variables: list[str] = Query(["wind_speed", "power"]),
):
    if "timestamp" in variables:
        raise HTTPException(
            status_code=400, detail="timestamp já é retornado automaticamente."
        )

    cols = ", ".join(["timestamp"] + variables)
    query = text(
        f"""
        SELECT {cols}
        FROM data
        WHERE timestamp BETWEEN :start AND :end
        ORDER BY timestamp
        """
    )
    df = pd.read_sql(query, engine, params={"start": start, "end": end})
    return df.to_dict(orient="records")
