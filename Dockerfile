# AI_BRIDGE - Production Container

FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    redis \
    sqlalchemy \
    psycopg2-binary \
    pyzmq

CMD ["python", "main.py"]
