from flask import Flask, render_template, jsonify, request
import requests
import constants

from twilio.access_token import AccessToken, IpMessagingGrant
from twilio.rest.ip_messaging import TwilioIpMessagingClient
from slackclient import SlackClient

import psycopg2
import psycopg2.extras


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
        text=message,
        username='Incoming:',
        )

    return r


def find_user_channel(user):

    print('finding channel for {0}'.format(user))

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
            INSERT INTO
                visitors (user_name, slack_channel, ipm_channel)
            VALUES
                (%s, %s, %s)
            """, (user, channel_id, ipm_channel))

        connection.commit()

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

