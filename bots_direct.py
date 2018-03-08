from chatterbot import ChatBot

maxxbot = ChatBot(
    'Maxxbot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./maxxbot.sqlite3'
)

am = ChatBot(
    'AM',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./am.sqlite3'
)

# Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")

# Get a response to an input statement
# chatbot.get_response("Hello, how are you today?")