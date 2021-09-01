FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#this line is mandatory if you did not set volumes in the .yml
ADD . /app 

# Run clean_databases.py when the container launches
CMD ["python", "clean_databases.py"]
