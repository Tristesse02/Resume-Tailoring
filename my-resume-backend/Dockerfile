FROM python:3.11-slim

# Prevent prompts during LaTeX install
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX and system dependencies
RUN apt-get update && \
    apt-get install -y texlive-full && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire backend app code
COPY . .

# Copy production environment file to .env
COPY deploy/.env .env

# Copy template resume file to app directory
COPY deploy/templateResume.j2 templateResume.j2

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "server.py"]
