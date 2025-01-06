# Use a minimal Python runtime as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app


COPY teadal-connectors/generated_servers /app/


COPY executor_test/ /app/executor_test/


RUN apt-get update && apt-get install -y  openssh-client git && rm -rf /var/lib/apt/lists/*

# TODO, Fix adding the repo to requirements-sfdps.txt and install it via docker build.
#RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
#RUN --mount=type=ssh git clone --depth=1 'git@github.ibm.com:<REPO>/executor-test.git'
#RUN cat ~/.ssh/known_hosts

# Install the Python dependencies
RUN --mount=type=ssh pip install --no-cache-dir -r requirements-sfdps.txt

ENV PYTHONPATH="/app/executor_test/:$PYTHONPATH"

# Expose the application port
EXPOSE 8000


# Run the FastAPI server using Uvicorn
CMD ["uvicorn", "generated_fastapi_app_fdp-czech-plant:app", "--host", "0.0.0.0", "--port", "8000"]
