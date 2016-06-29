from flask import Flask, render_template, jsonify, request
import time
import requests
import random, string
import constants
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from twilio.access_token import AccessToken, IpMessagingGrant
from slackclient import SlackClient

contact_bot = Flask(__name__)

# def get_bot_token():
#     identity = ''.join(random.choice(string.lowercase) for i in range(10))
#     endpoint = "TwilioChatDemo:{0}:{1}".format('contact_bot', identity)
#     token = AccessToken(
#         constants.TWILIO_ACCOUNT_SID,
#         constants.TWILIO_API_KEY,
#         constants.TWILIO_API_SECRET,
#         identity)
#     ipm_grant = IpMessagingGrant(endpoint_id=endpoint, service_sid=constants.TWILIO_SERVICE_SID)
#     token.add_grant(ipm_grant)
#
#     return token.to_jwt()


def handle_command(message, channel):
    response = message
    slack_client = SlackClient(constants.SLACK_BOT_TOKEN)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response, as_user=True
        )


def handle_response(message):
    client = TwilioIpMessagingClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)
    service = client.services.get(constants.TWILIO_SERVICE_SID)
    channel = service.channels.list()[-1]
    messages = channel.messages.create(body=message)

def handle_default_response(channel):
    print("default response")

    response = "Look -- I'm new here. And kind of stupid. Don't expect me to do much for now."
    slack_client = SlackClient(constants.SLACK_BOT_TOKEN)
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response, as_user=True
        )


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        print output_list
        for output in output_list:
            if output and 'text' in output and "echo" in output['text']:
                message = output['text'].split("echo")[1].strip().lower()

                return message, \
                       output['channel'], \
                       ""

            if output and 'text' in output and 'respond' in output['text']:
                message = output['text'].split('respond')[1].strip().lower()
                command = 'respond'

                return message, \
                       output['channel'], \
                       command

            if output and 'text' in output and constants.SLACK_AT_BOT in output['text']:

                return "", \
                       output['channel'], \
                       ""
    return None, None, None


if __name__ == "__main__":
    contact_bot.debug = True

    print(constants.SLACK_BOT_TOKEN)
    print(constants.SLACK_BOT_ID)

    slack_client = SlackClient(constants.SLACK_BOT_TOKEN)
    print(slack_client)

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
