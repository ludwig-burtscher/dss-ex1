FROM python:3.7-slim

RUN pip install pandas matplotlib
WORKDIR /app
COPY entrypoint.sh scripts /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

VOLUME /app/data/raw /app/data/output