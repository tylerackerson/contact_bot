import os
from flask import Flask, render_template, jsonify, request
from faker import Factory
from twilio.access_token import AccessToken, IpMessagingGrant
from slackclient import SlackClient
import contact_bot

app = Flask(__name__)
fake = Factory.create()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/incoming', methods=['POST'])
def incoming():
    generalChannel = os.environ['SLACK_CHANNEL']
    user = request.form.get('user')
    message = request.form.get('message')

    message = "User *{0}*: {1}".format(user, message)
    contact_bot.handle_command(message, generalChannel)
    return jsonify(response=message, user=user, company=company)


@app.route('/respond', methods=['POST'])
def respond():
    message = request.form["message"]
    print(message)

    return jsonify(message=message)


@app.route('/token')
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']
    service_sid = os.environ['TWILIO_IPM_SERVICE_SID']

    identity = fake.user_name()
    device_id = request.args.get('device')
    endpoint = "TwilioChatDemo:{0}:{1}".format(identity, device_id)
    token = AccessToken(account_sid, api_key, api_secret, identity)
    ipm_grant = IpMessagingGrant(endpoint_id=endpoint, service_sid=service_sid)
    token.add_grant(ipm_grant)

    bot_identity = 'contact_bot'
    bot_endpoint = "TwilioChatDemo:{0}:{1}".format(bot_identity, device_id)
    bot_token = AccessToken(account_sid, api_key, api_secret, bot_identity)
    bot_ipm_grant = IpMessagingGrant(endpoint_id=bot_endpoint, service_sid=service_sid)
    bot_token.add_grant(bot_ipm_grant)

    return jsonify(identity=identity, token=token.to_jwt(), bot_token=bot_token.to_jwt())


if __name__ == '__main__':
    app.debug = True
    app.run(port=3000)

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose

    if slack_client.rtm_connect():
        print("Contact Bot connected and running!")
        while True:
            message, channel, command = parse_slack_output(slack_client.rtm_read())
            if message and channel and command == 'respond':
                handle_response(message)
            if message and channel:
                handle_command(command, channel)
            elif channel:
                print('default')
                handle_default_response(channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
