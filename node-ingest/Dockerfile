FROM python:3.14-alpine

# Install mosquitto (which contains mosquitto_ctrl) and libedit
RUN apk update && \
    apk add --no-cache mosquitto libedit && \
    # Clean up the actual broker daemon to save space, keeping only the CLI tools
    rm -f /usr/sbin/mosquitto /usr/bin/mosquitto_passwd

WORKDIR /app

# Copy mosquitto init script and ingest script into the container
COPY docker-entrypoint.sh .
COPY ingest.py .

# Make the scripts executable
RUN chmod +x /app/docker-entrypoint.sh \
    && chmod +x /app/ingest.py

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to ensure Python output is sent straight away (unbuffered)
ENV PYTHONUNBUFFERED=1
#CMD ["python", "-u", "ingest.py"]
ENTRYPOINT ["/app/docker-entrypoint.sh"]