FROM python:3.14-alpine

# Install mosquitto (which contains mosquitto_ctrl) and libedit
RUN apk update && \
    apk add --no-cache mosquitto libedit && \
    # Clean up the actual broker daemon to save space, keeping only the CLI tools
    rm -f /usr/sbin/mosquitto /usr/bin/mosquitto_passwd

WORKDIR /app

# Copy mosquitto init script
COPY init-dynsec.sh .

# Make the script executable and run it to initialize the DynSec configuration
RUN chmod +x /init-dynsec.sh
RUN /init-dynsec.sh

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY ingest.py .

# Set environment variable to ensure Python output is sent straight away (unbuffered)
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "ingest.py"]