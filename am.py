import os
import time
import re
from slackclient import SlackClient
from chatterbot import ChatBot


# instantiate Slack client
slack_client = SlackClient(os.environ.get('AM_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

chatbot = ChatBot(
    'AM',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./am.sqlite3'
)

learn_list = []
last_message_ts = time.time()

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = parse_mention(event["text"])
            return message, event["channel"], event
    return None, None, None

def parse_mention(message_text):
    if "am" in message_text.lower():
        return message_text

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    # if command.startswith(EXAMPLE_COMMAND):
    #     response = "Sure...write some more code then I can do that!"

    response = chatbot.get_response(command)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def learn(event):
    global learn_list
    global last_message_ts
    message = event['text']
    ts = event['ts']
    time_since_last_message = ts - last_message_ts
    if time_since_last_message >= (12 * 60 * 60):
        chatbot.train(learn_list)
        print(learn_list)
        print('Trained list!')
        learn_list = []
    learn_list.append(message)
    print(learn_list)

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, event = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            if event:
                learn(event)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")