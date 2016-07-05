from flask import Flask, render_template, jsonify, request
from flask.ext.mysql import MySQL
from faker import Factory
from twilio.access_token import AccessToken, IpMessagingGrant
from twilio.rest.ip_messaging import TwilioIpMessagingClient
import contact_bot
import constants
import logging
from slackclient import SlackClient

app = Flask(__name__)
fake = Factory.create()

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'contact_bot'
app.config['MYSQL_DATABASE_HOST'] = constants.DB_HOST
mysql.init_app(app)

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

    conn = mysql.connect()
    cursor = conn.cursor()
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

        # currently ipm_channel is unicode -- needs to be string
        channel = service.channels.get(sid=ipm_channel)

        response = channel.messages.create(body=text)
    else:
        print('no ipm channel')

    return jsonify(response_type='in_channel', text=text)


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
