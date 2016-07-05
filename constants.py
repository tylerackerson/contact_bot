import os

SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_BOT_NAME =' contact_bot'
SLACK_BOT_ID = os.environ.get('SLACK_BOT_ID')
SLACK_USER_ID = os.environ.get('SLACK_USER_ID')

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_API_KEY = os.environ['TWILIO_API_KEY']
TWILIO_API_SECRET = os.environ['TWILIO_API_SECRET']
TWILIO_SERVICE_SID = os.environ['TWILIO_IPM_SERVICE_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']