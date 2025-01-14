# Use a minimal Python runtime as the base image
FROM registry.fedoraproject.org/f33/python3

# Set the working directory inside the container
WORKDIR /app


COPY generated_servers /app/

USER root

RUN yum -y install -y git && rm -rf /var/lib/apt/lists/*

# TODO, Fix adding the repo to requirements-sfdps.txt and install it via docker build.
RUN mkdir -p /root/.ssh && chmod 0700 /root/.ssh
RUN ssh-keyscan -t rsa github.ibm.com >> /root/.ssh/known_hosts

# Install the Python dependencies
RUN --mount=type=ssh,uid=1234  pip install --no-cache-dir -r requirements-sfdps.txt

ENV PYTHONPATH="/app/teadal_executor/:$PYTHONPATH"

# Expose the application port
EXPOSE 8000


# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "generated_fastapi_app_fdp-czech-plant:app", "--host", "0.0.0.0", "--port", "8000"]
