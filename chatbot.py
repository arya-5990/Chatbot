import logging
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

# Disable detailed logging
logging.basicConfig(level=logging.WARNING)

# Create chatbot
chatbot = ChatBot(
    "MyBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///mybot.sqlite3",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I'm sorry, I didn't quite understand that. Can you rephrase?",
            "maximum_similarity_threshold": 0.7,
        },
        "chatterbot.logic.TimeLogicAdapter",
    ]
)

# Train chatbot with the built-in corpus
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

# Train chatbot with custom responses
custom_trainer = ListTrainer(chatbot)
custom_conversations = [
    ["Hi", "Hello! How can I assist you today?"],
    ["What's your name?", "I am MyBot, your AI assistant."],
    ["What time is it?", "I can check the time for you!"],
    ["Tell me a joke", "Why don't skeletons fight each other? Because they don't have the guts!"],
    ["Goodbye", "Goodbye! Have a great day!"],
]
for convo in custom_conversations:
    custom_trainer.train(convo)

# Chat loop
print("Chatbot is running! Type 'quit' to exit.")
while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break

        response = chatbot.get_response(user_input)
        print("Chatbot:", response)

    except Exception as e:
        print("Chatbot: Sorry, I didn't understand that.")
