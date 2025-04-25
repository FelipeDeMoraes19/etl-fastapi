import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/source_db")

rng = pd.date_range("2024-04-01", periods=10 * 1440, freq="1min")

df = pd.DataFrame(
    {
        "timestamp": rng,
        "wind_speed": np.random.uniform(0, 20, size=len(rng)),
        "power": np.random.uniform(0, 100, size=len(rng)),
        "ambient_temperature": np.random.uniform(-10, 40, size=len(rng)),
    }
)

df.to_sql("data", engine, index=False, if_exists="append")
print("Dados inseridos:", len(df))
