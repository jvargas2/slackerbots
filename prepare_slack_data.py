import os
import json
import csv
import decimal

messages = []

for filename in os.listdir(os.getcwd() + '/slack_exports/maxxpotential/random'):
    day_data = json.load(open('slack_exports/maxxpotential/random/' + filename))
    for event in day_data:
        if event['type'] == 'message':
            if 'subtype' not in event:
                messages.append({'text': event['text'], 'ts': decimal.Decimal(event['ts'])})

messages = sorted(messages, key=lambda k: k['ts'])

time_since_last_message = decimal.Decimal(0)
last_message_ts = decimal.Decimal(1399226630.000000)
conversations = []
current_conversation = []

for m in messages:
    text = m['text']
    ts = m['ts']
    time_since_last_message = ts - last_message_ts
    if time_since_last_message >= (4 * 60 * 60):
        conversations.append(current_conversation)
        current_conversation = []
    current_conversation.append(text)
    last_message_ts = ts

conversations.append(current_conversation)

valid_conversations = []

for c in conversations:
    valid_c = []
    for m in c:
        if "http" not in m:
            valid_c.append(m)
    if len(valid_c) >= 2:
        valid_conversations.append(valid_c)

with open('slack_training_data.csv', 'w', newline='') as csvfile:
    cw = csv.writer(csvfile)

    for c in valid_conversations:
        cw.writerow(c)

print('Gathered ' + str(len(valid_conversations)) + ' valid conversations!')