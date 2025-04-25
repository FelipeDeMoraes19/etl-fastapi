from dagster import define_asset_job
from .assets import aggregated_signals

daily_job = define_asset_job(
    name="daily_etl_job",
    selection=[aggregated_signals]
)
