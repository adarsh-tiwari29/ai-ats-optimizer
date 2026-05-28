# 1. Base Python Image
FROM python:3.12-slim

# 2. Working directory setup
WORKDIR /app

# 3. Requirements copy aur install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Baaki saara frontend code copy karo
COPY . .

# 5. Streamlit ko port 8501 par expose karo
EXPOSE 8501

# 6. Streamlit chalu karne ki exact configuration command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]