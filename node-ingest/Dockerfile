FROM python:3

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY subscriber.py .

# Set environment variable to ensure Python output is sent straight away (unbuffered)
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "subscriber.py"]