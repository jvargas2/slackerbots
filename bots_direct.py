from chatterbot import ChatBot

maxxbot = ChatBot(
    'Maxxbot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./maxxbot.sqlite3'
)

am = ChatBot(
    'AM',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./am.sqlite3'
)

chatbot = am

# Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")

# Get a response to an input statement
# chatbot.get_response("Hello, how are you today?")

learn_list = []

def learn(message):
    global learn_list
    learn_list.append(message)
    if len(learn_list) >= 5:
        chatbot.train(learn_list)
        learn_list = []
    print(learn_list)

while True:
    m = input("> ")
    print(chatbot.get_response(m))
    learn(m)