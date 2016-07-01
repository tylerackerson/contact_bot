from flask import Flask, render_template, jsonify, request
from flask.ext.mysql import MySQL
import requests
import time
import random, string
import constants
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from twilio.access_token import AccessToken, IpMessagingGrant
from slackclient import SlackClient


contact_bot = Flask(__name__)

mysql = MySQL()

contact_bot.config['MYSQL_DATABASE_USER'] = 'root'
contact_bot.config['MYSQL_DATABASE_PASSWORD'] = ''
contact_bot.config['MYSQL_DATABASE_DB'] = 'contact_bot'
contact_bot.config['MYSQL_DATABASE_HOST'] = constants.DB_HOST
mysql.init_app(contact_bot)

def handle_incoming(message, user, ipm_channel):
    slack_client = SlackClient(constants.SLACK_BOT_TOKEN)
    channel_id = None

    if user == "system":
        return False

    channel_id = find_user_channel(user)

    if channel_id is None:
        channel_id = create_user_channel(user, ipm_channel)
    else:
        channel_id = channel_id[0]

    r = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message
        )

    return r


def find_user_channel(user):

    print('finding channel for {0}'.format(user))

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            slack_channel
        FROM
            visitors
        WHERE
            user_name = %s""", (user,))

    channel = cursor.fetchone()

    if channel:
        return channel

    return None


def create_user_channel(user, ipm_channel):
    slack_client = SlackClient(constants.SLACK_API_TOKEN)
    channel_name = "chat-{0}".format(user)

    r = slack_client.api_call(
        "groups.create",
        name=channel_name,
        )

    if r["ok"]:
        channel_id = r["group"]["id"]
        invite_to_channel(channel_id, constants.SLACK_USER_ID)

        # commit user + slack channel to DB
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO
                visitors
            SET
                user_name=%s,
                slack_channel=%s,
                ipm_channel=%s
            """, (user, channel_id, ipm_channel))

        conn.commit()

        return channel_id
    else:
        return None


def invite_to_channel(channel_id, user_id):
    slack_client = SlackClient(constants.SLACK_API_TOKEN)
    slack_bot = constants.SLACK_BOT_ID

    bot_r = slack_client.api_call(
        "groups.invite",
        channel=channel_id,
        user=slack_bot
        )

    print("invited bot channel: {0}".format(bot_r))

    r = slack_client.api_call(
        "groups.invite",
        channel=channel_id,
        user=user_id
        )

    if r["ok"]:
        print("invited to channel: {0}".format(channel_id))
        return r
    else:
        print("couldn't invite to channel")
        return r


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        print output_list

    return output_list


if __name__ == "__main__":
    contact_bot.debug = True
    mysql = MySQL(contact_bot)

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
