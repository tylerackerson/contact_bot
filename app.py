from flask import Flask, render_template, jsonify, request
from faker import Factory
from twilio.access_token import AccessToken, IpMessagingGrant
import contact_bot
import constants
from slackclient import SlackClient

app = Flask(__name__)
fake = Factory.create()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incoming', methods=['POST'])
def incoming():
    generalChannel = constants.SLACK_CHANNEL
    user = request.form.get('user')
    message = request.form.get('message')

    message = "User *{0}*: {1}".format(user, message)
    contact_bot.handle_command(message, generalChannel)
    return jsonify(response=message, user=user)


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
