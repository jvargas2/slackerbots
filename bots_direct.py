from chatterbot import ChatBot

am = ChatBot(
    'AM',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database='./am.sqlite3'
)

chatbot = am

l = []

# Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")

# Get a response to an input statement
# chatbot.get_response("Hello, how are you today?")

# learn_list = []

# def learn(message):
#     global learn_list
#     learn_list.append(message)
#     if len(learn_list) >= 5:
#         chatbot.train(learn_list)
#         learn_list = []
#     print(learn_list)

# for c in learn_list:
    # chatbot.train(c)

mode = 0

while mode <= 0:
    inp = int(input("Which mode? (1 - train, 2 - talk)\n> "))
    if inp <= 0:
        print('Wrong input. Please try again.')
    else:
        mode = inp

if mode == 1:
    print("Started training mode.")
    print("Will train the following list: ")
    print(l)
    print('Proceed? (y/n)')
    if input("> ") == 'y':
        chatbot.train(l)
    else:
        print('Cancelling...')

elif mode == 2:
    print("Started direct conversation mode.")
    while True:
        message = input("> ")
        print(chatbot.get_response(message))