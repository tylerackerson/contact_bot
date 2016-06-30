from flask import Flask, render_template, jsonify, request
import requests
import time
import random, string
import constants
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from twilio.access_token import AccessToken, IpMessagingGrant
from slackclient import SlackClient

contact_bot = Flask(__name__)


def handle_incoming(message, user):
    slack_client = SlackClient(constants.SLACK_BOT_TOKEN)

    # channel = find_user_channel(user) or create_user_channel(user)
    # channel_id = create_user_channel(user)

    print(channel_id)
    print(message)
    # slack_client.api_call(
    #     "chat.postMessage",
    #     channel=channel_id,
    #     text=message, as_user=True
    #     )

# def find_user_channel(user):
#     channel = None
#
#     # find channel for user in DB
#     # if not there return none
#
#     return channel


def create_user_channel(user):
    channel_name = "chat-{0}".format(user)

    create_channel_url = 'https://slack.com/api/channels.create?token={0}&name={1}&pretty=1'.format(
        constants.SLACK_API_TOKEN, channel_name)

    r = requests.post(create_channel_url)

    if r.status_code == requests.codes.ok:
        data = r.json()
        channel_id = data["channel"]["id"]
        invite_to_channel(channel_id)

        return channel_id
    else:
        return None


def invite_to_channel(channel_id):
    invite_to_channel_url = 'https://slack.com/api/channels.invite?token={0}channel={1}&user={2}pretty=1'.format(
        constants.SLACK_API_TOKEN, channel_id, 'U0J3TSVJA&')

    r = requests.post(invite_to_channel_url)
    data = r.json()

    if r.status_code == requests.codes.ok:
        print("invited to channel: {0}".format(channel_id))
        return jsonify(data=data)
    else:
        print("couldn't invite to channel")
        return jsonify(data=data)



def handle_response(message):
    client = TwilioIpMessagingClient(constants.TWILIO_ACCOUNT_SID, constants.TWILIO_AUTH_TOKEN)
    service = client.services.get(constants.TWILIO_SERVICE_SID)
    channel = service.channels.list()[-1]
    messages = channel.messages.create(body=message)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        print output_list

    return output_list


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
            parse_slack_output(slack_client.rtm_read())
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
