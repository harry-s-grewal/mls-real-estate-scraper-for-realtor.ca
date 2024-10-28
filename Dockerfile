# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Copy the requirements.txt file into the image
COPY requirements.txt .

# Install the dependencies using pip install -r requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the image
COPY . .

# Set the entry point to python
ENTRYPOINT ["python"]
