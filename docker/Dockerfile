# Step 1: define the base container
FROM python:3.10-slim

# Optionally: name the container
LABEL dataset="swe-bench-lite"
LABEL model="gpt-4o-mini"

# Step 2: Install system dependencies, including git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Step 2: config required environment variables
# Some config variables are hidden in .env file

# Step 3: ste working directory
WORKDIR /app

# Step 4: copy code into container
COPY . .

# Step 5: install required dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r ./docker/requirements.txt

# Step 9: Set the entrypoint
ENTRYPOINT ["bash", "docker/activate.sh"]