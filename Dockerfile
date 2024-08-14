# Set base image (host OS)
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install --upgrade pip

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# By default, listen on port 5000
EXPOSE 5000

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]