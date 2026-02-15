# 1. Base Image
FROM python:3.9-slim

# 2. Set working directory
WORKDIR /app

# 3. Install Dependencies
# We copy requirements from the backend folder
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Backend Code
COPY backend/app ./app

# 5. Copy Frontend Code
COPY frontend/ ./frontend

# 6. Set Environment Variable
ENV DOCKER_ENV=true

# 7. Run Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]