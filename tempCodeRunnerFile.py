#importing required libraries

import pyperclip #Detects selected words
import requests #Sends HTTP requests to dictionary API
from pynput import keyboard as pkb
from pync import Notifier  # For macOS notifications
import subprocess
import os




#Function to fetch the word definition from Dictionary API
def fetch_definition(word):

#Exception Handling
#Try to find the word, if not then skip to the except block
    try: 
        #send a get request to the dictionary api with the given word
        response=requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        #Checking if the fetch was successful
        if response.ok:

            #The dictionary api send the response back as a json file 
            data=response.json() # .json() function converts in the form of python list and dictionaries
            
            return data[0]['meanings'][0]['definitions'][0]['definition']

#If the code inside try fails - network error, invalid json, missing data, any exception
    except:
        return "Error fetching definition"

#If try block executes and nothing is returned - this line executes
    return "Definition not found."


def show_mac_notification(title, message):
    message = message.replace('"', '\\"')
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])




#Function is called when hot-key is pressed
def on_activate():
    word=pyperclip.paste().strip() #gets the text on the clip board and removes leading or trailing spaces
    print(f"Hotkey triggered. Word copied: {word}")
    if word:
        definition=fetch_definition(word)
        print(f"Definition: {definition}")
        show_mac_notification("Definition", definition)


# Let the user know the tool is running
print("AI Dictionary Tool is running... Press Ctrl+Alt+D after copying a word.")




with pkb.GlobalHotKeys({
    '<ctrl>+<alt>+d': on_activate
}) as h:
    h.join()
