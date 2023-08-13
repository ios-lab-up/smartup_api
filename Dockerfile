FROM python:3.10.7-bullseye

# Set the working directory in the container to /SmartUP
WORKDIR /SmartUP

# Copy all necessary files
COPY . .

# Download Google Chrome and Chrome Driver concurrently using curl with -OJ option
RUN curl -OJ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    curl -OJ https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/

# Install all dependencies
RUN apt update && \
    apt install -y ./google-chrome-stable_current_amd64.deb unzip && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Set environment variables
ENV FLASK_DEBUG=development \
    DEBUG=true \
    DISPLAY=:99

# Run the command to start your application
CMD ["python", "App/run.py"]

# Expose port 5555
EXPOSE 5555
