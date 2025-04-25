FROM python:3.11-slim 

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir dagster dagster-webserver

RUN pip install --no-cache-dir -r etl/requirements.txt

ENV DAGSTER_HOME=/app/dagster_home
RUN mkdir -p $DAGSTER_HOME && touch $DAGSTER_HOME/dagster.yaml

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-w", "etl_orch/workspace.yaml"]
