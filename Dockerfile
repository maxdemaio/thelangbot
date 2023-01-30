FROM python:3.9

# Install cron and other needed packages
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /

# Copy required files
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the bot.py fle
COPY bot.py .

# Add a cron job to execute bot.py every 10 minutes
RUN echo "*/10 * * * * cd / && python bot.py" >> /etc/crontab

# Start the cron service
CMD ["cron", "-f"]
