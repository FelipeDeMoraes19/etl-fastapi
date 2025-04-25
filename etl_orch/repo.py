from dagster import Definitions

from etl_orch.assets import aggregated_signals
from etl_orch.jobs import daily_job
from etl_orch.schedules import daily_schedule
from etl_orch.resources import source_api, target_engine

defs = Definitions(
    assets=[aggregated_signals],
    jobs=[daily_job],
    schedules=[daily_schedule],
    resources={"source_api": source_api, "target_engine": target_engine},
)
