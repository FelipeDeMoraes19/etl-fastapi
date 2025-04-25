from dagster import asset, DailyPartitionsDefinition
import pandas as pd
from sqlalchemy.orm import Session
from etl.models import Signal


partitions = DailyPartitionsDefinition(start_date="2024-04-01")


@asset(
    partitions_def=partitions,
    required_resource_keys={"source_api", "target_engine"},
    io_manager_key=None,  
)
def aggregated_signals(context):
    date = context.partition_key  

    r = context.resources.source_api.get(
        "", params={
            "start": f"{date}T00:00:00",
            "end":   f"{date}T23:59:59",
            "variables": ["wind_speed", "power"],
        }
    )
    r.raise_for_status()
    df = pd.DataFrame(r.json())

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    agg = (
        df.resample("10min")
          .agg(["mean", "min", "max", "std"])
          .rename_axis("timestamp")
    )
    agg.columns = [f"{v}_{stat}" for v, stat in agg.columns]
    agg.reset_index(inplace=True)

    with Session(context.resources.target_engine) as sess:
        for _, row in agg.iterrows():
            ts = row["timestamp"]
            for col in agg.columns[1:]:
                sess.add(
                    Signal(
                        name=col,
                        timestamp=ts,
                        signal_id=hash(col) % 1000,
                        value=row[col],
                    )
                )
        sess.commit()

    context.log.info(f"Inserido: {len(agg)* (len(agg.columns)-1)} linhas")
