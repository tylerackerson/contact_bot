import os
from flask import Flask, render_template, jsonify, request
from faker import Factory
from twilio.access_token import AccessToken, IpMessagingGrant
import contact_bot

app = Flask(__name__)
fake = Factory.create()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incoming', methods=['POST'])
def incoming():
    user = request.form.get('user')
    message = request.form.get('message')

    message = "User *{0}*: {1}".format(user, message)
    contact_bot.handle_command(message, 'C1EU7HEH0')
    return jsonify(response=message, user=user, company=company)


@app.route('/respond', methods=['POST'])
def respond():
    response = request.form.get('response')
    user = request.form.get('user')
    company = request.form.get('company')

    message = "From {0} who works at {1}: {2}".format(user, company, response)
    contact_bot.handle_command(message, 'C1EU7HEH0')
    return jsonify(response=response, user=user, company=company)

@app.route('/token')
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']
    service_sid = os.environ['TWILIO_IPM_SERVICE_SID']

    # create a randomly generated username for the client
    identity = fake.user_name()

    # Create a unique endpoint ID for the
    device_id = request.args.get('device')
    endpoint = "TwilioChatDemo:{0}:{1}".format(identity, device_id)

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity)

    # Create an IP Messaging grant and add to token
    ipm_grant = IpMessagingGrant(endpoint_id=endpoint, service_sid=service_sid)
    token.add_grant(ipm_grant)

    # Return token info as JSON
    return jsonify(identity=identity, token=token.to_jwt())


if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)