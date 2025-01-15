# Use a minimal Python runtime as the base image
FROM registry.redhat.io/ubi9/python-312

# Set the working directory inside the container
WORKDIR /app

USER root

RUN yum -y install -y git && rm -rf /var/lib/apt/lists/*

# TODO, Fix adding the repo to requirements-sfdps.txt and install it via docker build.
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
RUN ssh-keyscan -t rsa github.ibm.com >> /root/.ssh/known_hosts

# Install the Python dependencies
COPY generated_servers /app/
COPY transform /app/

RUN --mount=type=ssh  pip install --no-cache-dir -r requirements-sfdps.txt

# Expose the application port
EXPOSE 8000

# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "generated_fastapi_app_fdp-czech-plant:app", "--host", "0.0.0.0", "--port", "8000"]
