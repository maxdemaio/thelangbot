import os
from flask import Flask

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


if __name__ == '__main__':
    app.run(os.getenv("PORT"))
