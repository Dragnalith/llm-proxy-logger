FROM python:3.11-slim

WORKDIR /app

RUN pip install litellm[proxy]

COPY config.yaml .
COPY logger.py .
COPY run_proxy.py .

EXPOSE 4000

CMD ["python", "run_proxy.py"]