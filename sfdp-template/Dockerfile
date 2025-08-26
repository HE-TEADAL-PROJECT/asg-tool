# syntax=docker/dockerfile:1.3
FROM registry.teadal.ubiwhere.com/teadal-public-images/asg-runtime:0.0.1

# Set working directory
WORKDIR /app

# Update pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
COPY pyproject.toml ./
COPY README.md ./
RUN pip install --no-cache-dir ".[cache-disk,cache-redis,logging-rich,logging-json]"

# Copy app source code
COPY app.py .
COPY transforms ./transforms

# Use non-root user
RUN useradd -m appuser
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]