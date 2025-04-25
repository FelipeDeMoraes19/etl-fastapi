from dagster import ScheduleDefinition
from .jobs import daily_job

daily_schedule = ScheduleDefinition(
    job=daily_job,
    cron_schedule="0 2 * * *",  
)
