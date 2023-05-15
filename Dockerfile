# FROM python:3.10.7-buster
# WORKDIR /SmartUP
# COPY . .
# ENV FLASK_ENV development
# ENV DEBUG true
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# RUN apt-get install -y wget
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# # Unzip the Chrome Driver into /usr/local/bin directory
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# # Set display port as an environment variable
# ENV DISPLAY=:99

# RUN pip install --upgrade pip && pip3 install -r requirements.txt
# CMD ["python", "App/run.py"]

# # Makes the file executable
# EXPOSE 5555
# Use an official Python runtime based on Debian Buster as a parent image
FROM python:3.10.7-bullseye

# Set the working directory in the container to /SmartUP
WORKDIR /SmartUP

# Copy only the necessary files first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install any necessary dependencies 
RUN apt-get update && pip install --upgrade pip && pip3 install -r requirements.txt

# Download Google Chrome and Chrome Driver concurrently
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb & \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip & \
    wait

# Install Google Chrome and Chrome Driver
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    ; unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copy the rest of your application's necessary files
COPY . .

# Set environment variables
ENV FLASK_ENV development
ENV DEBUG true
ENV DISPLAY=:99

# Run the command to start your application
CMD ["python", "App/run.py"]

# Expose port 5555
EXPOSE 5555
