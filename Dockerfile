#1. Base iMage
FROM ubuntu:22.04

# 2. Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# DEBIAN_FRONTEND=noninteractive prevents apt from hanging on timezone prompts
ENV DEBIAN_FRONTEND=noninteractive 

# 3. Work Directory
WORKDIR /app

# 4. Install System Dependencies (Python + Pip)
# We clean up apt lists afterwards to keep the image size smaller
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
COPY requirements.txt .
# Note: On Ubuntu, we typically use 'pip3' instead of 'pip'
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install gunicorn

# 6. Copy Application Code
COPY . .

# 7. Create a Non-Root User
# Ubuntu has 'adduser', so this syntax still works perfectly
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# 8. Switch to Non-Root User
USER appuser

# 9. Exposure
EXPOSE 8000

# 10. Command
# We use python3 -m gunicorn to ensure we find the installed package
CMD ["python3", "-m", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]