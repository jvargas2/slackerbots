from chatterbot import ChatBot
import csv

def teach_english(chatbot):
    proceed = input('Teach English? (y/n)\n> ')
    if proceed == 'y':
        chatbot.train("chatterbot.corpus.english")
        print('Training complete.')
    else:
        print('Cancelling...')

def teach_slack(chatbot):
    with open('slack_training_data.csv') as csvfile:
        cr = csv.reader(csvfile)
        proceed = input('Slack training data ready. Proceed? (y/n)\n> ')
        conversation_count = 0
        if proceed == 'y':
            for row in cr:
                print('Training conversation ' + str(conversation_count))
                chatbot.train(row)
                conversation_count += 1
            print(str(conversation_count) + ' conversations trained!')
        else:
            print('Cancelling...')

valid_training_types = ['corpus', 'slack']

bot_name = input('Which bot you are training? (Maxxbot, AM)\n> ')

if bot_name == 'Maxxbot' or bot_name == 'AM':
    training_type = input('What trainer are you using? (corpus, slack)\n> ')
    
    if training_type in valid_training_types:
        database = './' + bot_name.lower() + '.sqlite3'
        trainer = ''

        if training_type == 'corpus':
            trainer = 'ChatterBotCorpusTrainer'
        else:
            trainer = 'ListTrainer'

        chatbot = ChatBot(
            bot_name,
            trainer='chatterbot.trainers.' + trainer,
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database=database
        )

        if training_type == 'corpus':
            teach_english(chatbot)
        elif training_type == 'slack':
            teach_slack(chatbot)
    else:
        print('Not a valid trainer. Try again.')
else:
    print('Not a valid bot name. Try again.')