FROM python:3.9

# Install cron and other needed packages
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /app

# Copy the app directory contents into the container at /app
COPY app/ /app/

# Copy hello-cron file to the cron.d directory
COPY app/bot-cron /etc/cron.d/bot-cron

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/bot-cron

# Apply cron job
RUN crontab /etc/cron.d/bot-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the cron job on container startup
CMD cron && tail -f /var/log/cron.log
