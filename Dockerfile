FROM python:3.9

# Install cron and other needed packages
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /app

# Copy the app directory contents into the container at /app
COPY app/ /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set up the cron job
RUN echo "*/10 * * * * /usr/local/bin/python /app/bot.py" >> /etc/crontab

# Start the cron service
CMD ["cron", "-f"]
