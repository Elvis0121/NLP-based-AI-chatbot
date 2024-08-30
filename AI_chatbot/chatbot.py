# imports for hard-coded rule bot

import re
import random

# imports for dynamic bot
import numpy as np
import nltk
import string
# import random
import sklearn.feature_extraction.text as sk_text
import sklearn.metrics.pairwise as sk_pair
#imports for printing out on the console
import os
import time
import sys

# chatbot rules class
class RuleBot(object):
    # potential negative responses to train the model
    negative_responses = ["no", "sorry", "nope", "meh", "not a chance", "nah", "naw"]
    # keywords for when the user wants to end the conversation
    exit_keywords = ["end", "quit", "bye", "goodbye", "done"]
    # starter questions
    starter_questions = [
        "How may I help you?\n",
        "What's your favorite dish?\n",
        "What technology do you use daily?\n",
        "What's the Earth's surface area?\n",
    ]

    def __init__(self):
        self.babble = {
            "describe_planet_intent": r".*\s*your planet.*",
            "why_question": r"why\sare.*",
            "new_knowledge": r"*\s*knowledge"}
    
    def greet(self):
        # get user's name
        self.name = input("What's your name?\n")
        # check whether or not user wants to chat
        wants_to_chat = input(f"Hi {self.name}! I am a chatbot from another planet. Will you help me learn more about the Earth?\n")
        if wants_to_chat in self.negative_responses:
            print("That's alright. Goodbye!")
            return
        # chatting if wants_to_chat
        self.chat()

    def exit_conversation(self, response):
        if response in self.exit_keywords:
            print("Ok. Have a nice day!")
            return True
    
    def chat(self):
        response = input(random.choice(self.starter_questions)).lower() # ask a question and get a response
        while not self.exit_conversation(response):
            response = input(self.respond(response))
    
    def respond(self, response):
        for k, v in zip(self.babble.keys(), self.babble.values()):
            intent, regex_pattern = k, v
            matching = re.match(regex_pattern, response)
            if matching:
                if intent == "describe_planet_intent": return self.describe_planet_intent()
                elif intent == "why_question": return self.why_question()
                elif intent == "new_knowledge": return self.new_knowledge()
            else: return self.no_matching_intent()

    # intents
    def describe_planet_intent(self):
        responses = [
            "Howdy y'all! This is PlanetBot.\n",
            "Aloha! I am a bot from another planet!\n",
            "Ni hau ma!\n",
            "Como es tas!\n",
        ]
        return random.choice(responses)
    
    def why_question(self):
        responses = [
            "Looking to make new friends. I hear the people on this planet are friendly.\n",
            "I am excited to try your water. Must taste nice!\n",
            "I'd like to swim in your swimming pools!\n",
            "There are roads on this planet!\n"
        ]
        return random.choice(responses)
    
    def new_knowledge(self):
        responses = [
            "Learning comes in many different forms. I am a bot trying to learn via NLP!\n",
            "Bots are more likely to help improve the status quo on your planet, than destroy it.\n",
            "Natural Language Processing is pertinent in AI/ML.\n"
        ]
        return random.choice(responses)
    
    def no_matching_intent(self):
        responses = [
            "Why do you think so?\n",
            "Do you care to elaborate?\n",
            "Would you please expand on that?\n",
            "Tell me more!\n",
            "Is that true?\n",
        ]
        return random.choice(responses)

# alien_robot = RuleBot()
# alien_robot.greet()






# dynamic bot
nltk.download("punkt") # Punkt tokenizer
nltk.download("wordnet") # dictionary of words
nltk.download("omw-1.4")

with open("chatbot_spiel.txt", "r", errors = "ignore") as file:
    raw_document = file.read()
    raw_document = raw_document.lower() # change all text to lowercase

tokenized_sentences = nltk.sent_tokenize(raw_document)
tokenized_words = nltk.word_tokenize(raw_document)
lemma = nltk.stem.WordNetLemmatizer() # text normalization technique to group inflected forms of words together eg dog, dogs

# word cleaning/preprocessing
def LemmaTokens(tokens):
    """
    Gets all the word tokens stemming from the same base form.
    """
    output = []
    for token in tokens:
        output.append(lemma.lemmatize(token))
    return output

punctuation_dictionary = {}
for punctuation in string.punctuation:
    punctuation_dictionary[ord(punctuation)] = None

def LemmaNormalize(text):
    """
    Dump.
    """
    return LemmaTokens(nltk.word_tokenize(text.lower().translate(punctuation_dictionary)))


dynamic_bot_greetings = ["hi", "howdy", "hello", "wassup", "sup", "yhoo"]
dynamic_bot_greeting_responses = ["great thanks", "sup", "hello there", "hey", "hi"]
dynamic_bot_exit_keywords = ["end", "quit", "bye", "goodbye", "done"]
dynamic_bot_negative_responses = ["no", "sorry", "nope", "meh", "not a chance", "nah", "naw"]
# greeting the user
def dynamic_bot_greet(user_input):
    for word in user_input.lower().split():
        if word in dynamic_bot_greetings:
            return random.choice(dynamic_bot_greeting_responses)

def dynamic_bot_response(user_input):
    bot_response = ""
    vector = sk_text.TfidfVectorizer(tokenizer = LemmaNormalize, stop_words= "english")
    tfidf = vector .fit_transform(tokenized_sentences)
    similarity_values = sk_pair.cosine_similarity(tfidf[-1], tfidf)
    index = similarity_values.argsort()[0][-2]
    flattened_values = similarity_values.flatten()
    flattened_values.sort()
    required_tfidf = flattened_values[-2]
    if required_tfidf == 0:
        return (bot_response + "Sorry, I do not understand what you're trying to put across. :(")
    return (bot_response + tokenized_sentences[index])

def dynamic_bot_typeWrite(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

# flow of conversation
# def start_conversing():
keep_conversing = True # indicator to determine whether or not to continue the conversation
welcome_text = "\nHi! I am a prototype learning bot being developed by Elvis.\nLet's talk!"
dynamic_bot_typeWrite(welcome_text)
while keep_conversing:
    user_response = input("\nUser: ").lower()
    if user_response in dynamic_bot_exit_keywords:
        keep_conversing = False
        end_text = "thank you for chatting. Bye!"
        print("Bot: ")
        dynamic_bot_typeWrite(end_text)

    else:
        if user_response in {"thanks", "thank you"}:
            keep_conversing = False
            print("Bot: ")
            dynamic_bot_typeWrite("You're welcome!")
        elif user_response in dynamic_bot_greetings:
            print("Bot: ")
            dynamic_bot_typeWrite(dynamic_bot_greet(user_response))
        else:
            # learn from user input
            tokenized_sentences.append(user_response)
            tokenized_words = tokenized_words + nltk.word_tokenize(user_response)
            all_words = list(set(tokenized_words))
            print("Bot: ", )
            dynamic_bot_typeWrite(dynamic_bot_response(user_response))
            tokenized_sentences.remove(user_response)

# if __name__ == "__main__":
#     start_conversing()