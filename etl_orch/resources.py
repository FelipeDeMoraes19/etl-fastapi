from dagster import resource
from sqlalchemy import create_engine
import httpx

SOURCE_URL = "http://api:8000/data/"
TARGET_URL = "postgresql://user:password@target_db:5432/target_db"


@resource
def source_api(_):
    return httpx.Client(base_url=SOURCE_URL, timeout=30.0)


@resource
def target_engine(_):
    return create_engine(TARGET_URL, future=True)
