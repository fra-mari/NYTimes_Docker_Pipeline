FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
COPY requirements.txt /app 

#this line is mandatory if you did not set volumes in the .yml
ADD . /app 

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run get_tweets.py when the container launches
CMD ["python", "get_tweets.py"]
