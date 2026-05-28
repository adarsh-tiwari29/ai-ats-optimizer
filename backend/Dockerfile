# 1. Base Python Image
FROM python:3.12-slim

# 2. Container ke andar working directory set karo
WORKDIR /app

# 3. System level dependencies install karo (PDF and Network optimization ke liye)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. requirements.txt copy karo aur libraries install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Baaki saara backend ka code copy karo
COPY . .

# 6. FastAPI ko port 8000 par expose karo
EXPOSE 8000

# 7. Server start karne ki command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]