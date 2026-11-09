FROM python:3.12-slim

WORKDIR /opt/tickets

RUN useradd --uid 10003 --no-create-home runner \
    && mkdir -p /data \
    && chown -R runner:runner /opt/tickets /data

COPY app.py .

RUN chown runner:runner app.py

USER runner

EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8003/health')"

CMD ["python", "app.py"]