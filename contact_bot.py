import os
import time
from slackclient import SlackClient

BOT_ID = os.environ.get('BOT_ID')

AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "echo"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('BOT_ID'))

def handle_command(command, channel):
    response = command
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response, as_user=True
        )

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
            if output and 'text' in output and EXAMPLE_COMMAND in output['text']:
                command = output['text'].split(EXAMPLE_COMMAND)[1].strip().lower()
                return command, \
                       output['channel']
            if output and 'text' in output and AT_BOT in output['text']:
                return "", \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Contact Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            elif channel:
                print('default')
                handle_default_response(channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")