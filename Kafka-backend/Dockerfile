# Step 1: Specify the base image
FROM python:3

# Step 2: Copy the application files
COPY . /app

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Install dependencies
RUN pip install -r requirements.txt

EXPOSE 8080

# Step 6: Define the startup command
CMD ["python", "main.py"]

