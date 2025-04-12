FROM python:3.11-slim

# Prevent prompts during LaTeX install
ENV DEBIAN_FRONTEND=noninteractive

# Install LaTeX packages and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        texlive-latex-base \
        texlive-fonts-recommended \
        texlive-latex-recommended \
        texlive-latex-extra \
        ghostscript \
        make \
        && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Run your Flask app
CMD ["python", "server.py"]
