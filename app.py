from flask import Flask, render_template, jsonify, request
from faker import Factory
import contact_bot
import constants
import logging

from twilio.access_token import AccessToken, IpMessagingGrant
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from slackclient import SlackClient

import psycopg2
import psycopg2.extras
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine


app = Flask(__name__)
fake = Factory.create()
app.config['SQLALCHEMY_DATABASE_URI'] = constants.DB_HOST
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incoming', methods=['POST'])
def incoming():
    user = request.form.get('user')
    message = request.form.get('message')
    ipm_channel = request.form.get('ipm_channel')

    message = "User *{0}*: {1}".format(user, message)
    contact_bot.handle_incoming(message, user, ipm_channel)

    return jsonify(incoming=message, user=user, ipm_channel=ipm_channel)


@app.route('/respond', methods=['POST'])
def respond():
    if not request.form.get('token'):
        return json("no token")

    channel_id = request.form.get('channel_id')
    text = request.form.get('text')

    # local DB HOST
    connection_data = "host={0} dbname={1} user={2} password={3}".format(
        constants.DB_HOST,
        constants.DB_NAME,
        constants.DB_USER,
        constants.DB_PASS
    )

    print "Connecting to database\n	->%s" % (connection_data)
    connection = psycopg2.connect(connection_data)
    cursor = connection.cursor()
    print "Connected!\n"

    cursor.execute("""
        SELECT
            ipm_channel
        FROM
            visitors
        WHERE
            slack_channel = %s""", (channel_id,))

    ipm_channel = cursor.fetchone()

    if ipm_channel:
        ipm_channel = ipm_channel[0]

        client = TwilioIpMessagingClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)
        service = client.services.get(constants.TWILIO_SERVICE_SID)
        channel = service.channels.get(sid=ipm_channel)

        response = channel.messages.create(body=text)
    else:
        print('no ipm channel')

    return jsonify(text=text)


@app.route('/token')
def token():
    identity = fake.user_name()
    device_id = request.args.get('device')
    endpoint = "TwilioChatDemo:{0}:{1}".format(identity, device_id)
    token = AccessToken(
        constants.TWILIO_ACCOUNT_SID,
        constants.TWILIO_API_KEY,
        constants.TWILIO_API_SECRET,
        identity)
    ipm_grant = IpMessagingGrant(endpoint_id=endpoint, service_sid=constants.TWILIO_SERVICE_SID)
    token.add_grant(ipm_grant)

    return jsonify(identity=identity, token=token.to_jwt())


if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
