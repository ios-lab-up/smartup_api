FROM python:3.10.7-bullseye

# Set the working directory in the container to /SmartUP
WORKDIR /SmartUP

# Copy all necessary files
COPY . .

# Install all dependencies
RUN apt update && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    apt-get install -y firefox-esr && \
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
