FROM python:3.9

# Install cron and other needed packages
RUN apt-get update && apt-get install -y cron

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add a cron job to execute bot.py every 10 minutes
RUN echo "*/10 * * * * cd /app && python bot.py" >> /etc/crontab

# Start the cron service
CMD ["cron", "-f"]
