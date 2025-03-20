# Use Conda base image
FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /app

# Copy environment file
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Initialize conda in bash
RUN conda init bash

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Activate conda environment and run the application
SHELL ["/bin/bash", "-c"]
CMD ["conda", "run", "-n", "lwk-scraping", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
