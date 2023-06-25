import threading
import tkinter as tk
import pyautogui
import keyboard

input_label = None
your_text_entry = None
username_entry = None
detectedLetter = None
currentInput = []
userText = []
labels = []
with open('C:\\Users\\Tal\\Desktop\\Tal\\Study\\Study\\finalProject\\SIGNiT\\Model\\labels.txt', 'r') as file:
    for line in file:
        index, label = line.strip().split(' ', 1)
        labels.append(label)

hebrewLabels = ["ע", "א", "ב", ",",
          "ד", "Delete", ".", "ג", "ח", "ה", "כ", "ק", "ל", "מ", "נ", "פ", "?",
          "ר", "ס", "ש", " ", "ת", "ט", "צ", "Use", "ו", "י", "ז"]

labels_map = dict(zip(labels, hebrewLabels))
suffix_map = dict([('כ','ך'),('מ','ם'),('פ','ף'),('צ','ץ')])

def getWord():
    global currentInput
    return ''.join(currentInput)      

def addWord2Text():
    global your_text_entry, userText
    convertSuffix()
    userText.append(getWord())
    setYourText()
    clearInput()

def convertSuffix():
    global currentInput, suffix_map
    if currentInput:
        ch = currentInput[-1]
        if ch in ['כ', 'מ', 'פ', 'צ']:
            currentInput.pop()
            currentInput.append(suffix_map[ch]) 

        



def setYourText():
    global your_text_entry, userText
    your_text_entry.delete(0, tk.END)  # Remove existing text
    your_text_entry.insert(0, " ".join(userText))  # Set new text
    clearInput()

def addInputLetter(ch = None):
    global currentInput, detectedLetter
    # Convert to Hebrew
    currentInput.append(convert2Heb(detectedLetter))
    setInputLabel()
    
def setInputLabel():
    global input_label, currentInput
    input_label.configure(text= ' - '.join(currentInput))

def addWord2YourText():
    thread = threading.Thread(target=addWord2Text)
    thread.start()

def addLetter2Input():
    thread = threading.Thread(target=addInputLetter)
    thread.start()

def convert2Heb(letter):
    return labels_map[letter]

def clearInput():
    global currentInput
    currentInput.clear()
    setInputLabel()

def deleteLastInputLetter():
    global currentInput, userText
    if currentInput:
        # Remove last char
        currentInput.pop()  
        setInputLabel()
    elif userText:
        # Remove last word
        remove_last_word()
        setYourText()

def remove_last_word():
    global userText
    userText.pop() # Remove last word

def handelInput(sign):
    if not sign:
        return
    elif sign == "Space":
        # Add space + start new word
        addWord2Text()
    elif sign == "Comma":
        # Add comma to the end of word and start new word
        convertSuffix()
        addInputLetter(",")
        addWord2Text()
    elif sign == "Use":
        # TODO: Use Autocomplete
        return
    elif sign == "Delete":
        # Delete input letter
        deleteLastInputLetter()
    elif sign == "Dot":
        # Add Dot to the end of word and start new sentence
        convertSuffix()
        addInputLetter(".\n")
        addWord2Text()
    else:
        # Add last char to input
        addLetter2Input()
          
    
     






