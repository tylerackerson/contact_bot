import os
import time
import requests
# from slackclient import SlackClient

BOT_ID = os.environ.get('BOT_ID')
BOT_NAME ='contact_bot'

AT_BOT = "<@" + BOT_ID + ">:"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('BOT_ID'))

def handle_command(message, channel):
    response = message
    # print("channel: {0}".format(channel))
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response, as_user=True
        )


def handle_response(message):
    r = requests.post ('http://localhost:3000/respond', data={'message': message})
    # create IP messaging response from bot from here


def handle_default_response(channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    print("default response")

    response = "Look -- I'm new here. And kind of stupid. Don't expect me to do much for now."
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response, as_user=True
        )


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
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

            if output and 'text' in output and AT_BOT in output['text']:

                return "", \
                       output['channel'], \
                       ""
    return None, None, None


# if __name__ == "__main__":
#     READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
#
#     if slack_client.rtm_connect():
#         print("Contact Bot connected and running!")
#         while True:
#             message, channel, command = parse_slack_output(slack_client.rtm_read())
#             if message and channel and command == 'respond':
#                 handle_response(message)
#             if message and channel:
#                 handle_command(command, channel)
#             elif channel:
#                 print('default')
#                 handle_default_response(channel)
#             time.sleep(READ_WEBSOCKET_DELAY)
#     else:
#         print("Connection failed. Invalid Slack token or bot ID?")
