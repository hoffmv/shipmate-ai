FROM python:3.13-slim

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "shipmate_full_daily_plan.py"]
