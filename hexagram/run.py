import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app()

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    app.run()