import json
from difflib import get_close_matches
import sys
import time

exit_keywords = ["end", "quit", "bye", "goodbye", "done"]

# load the knowledge base from the JSON file
def load_knowledge_base(file_path):
    with open(file_path) as file:
        knowledge = json.load(file)
    return knowledge

# save responses from previous responses in knowledge base
def save_knowledge_base(file_path, data):
    with open(file_path ,"w") as file:
        json.dump(data, file, indent = 2)

def optimal_match(question, database):
    """
    Finds the best matching question from the knowledge base and returns its corresponding response.
    """
    matching_questions = get_close_matches(question, database, n = 1, cutoff = 0.6) # n = 1 returns the best answer possible, cutoff is accuracy score
    if matching_questions: return matching_questions[0]

def fetch_response(question, knowledge_base):
    """
    Gets an answer to a given question if it exists. Else returns None.
    """
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def typeWriter(text):
    """
    Outputs text onto the console like a type writer.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    print() # prints a new line at the end of the text. Stylistic choice

    
def chatBot():
    knowledge_base = load_knowledge_base("/Users/chipiro/Desktop/random/ai/knowledge_base.json")
    fail_message = "I do not know what that means :( - please help me learn."
    learn_answer_message = "Please type the answer, or 'skip' to skip."
    learn_thank_you = "Thank you for teaching me something new! Now I know :) "
    while True: # infinite loop for chatting
        user_input = input("You: ")
        if user_input.lower() in exit_keywords: break
        # find the best matching question from the user
        best_match = optimal_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match is not None:
            response = fetch_response(best_match, knowledge_base)
            typeWriter("Bot: " + response)
        else:
            typeWriter("Bot: " + fail_message)
            typeWriter(learn_answer_message)
            answer = input()
            if answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": answer})
                save_knowledge_base("/Users/chipiro/Desktop/random/ai/knowledge_base.json", knowledge_base)
                typeWriter(learn_thank_you)

if __name__ == "__main__":
    chatBot()

