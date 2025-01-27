import re
import pyttsx3
import json
import configparser

# Initialize pyttsx3 engine for TTS
engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} (ID: {voice.id})")

voice_name = "Microsoft Sam"  

custom_words_path = "C:/Users/cheezy/Documents/tf2 tts/custom_words.json" #path to this file

def load_custom_words():
    try:
        with open(custom_words_path, 'r') as file:
            word_list = json.load(file).get('custom_word_list', [])
            return word_list
    except FileNotFoundError:
        print("Error: file not found")
        return []

def replace_custom_words(chat_message, custom_words):
    print(f"Original chat message: {chat_message}")  
    for word in custom_words:
        if word["symbol"] in chat_message:
            print(f"Replacing '{word['symbol']}' with '{word['response']}'") 
            chat_message = chat_message.replace(word["symbol"], word["response"])
    print(f"Modified chat message: {chat_message}") 
    return chat_message

custom_words = load_custom_words()

if not isinstance(custom_words, list):
    print("Error: custom_words is not a list!")
else:
    print(f"Loaded custom words: {custom_words}")

# Set the voice
for voice in voices:
    if voice.name == voice_name:
        engine.setProperty('voice', voice.id)
        print(f"Voice set to: {voice_name}")
        break

# Set speech rate and volume
engine.setProperty('rate', 175)  
engine.setProperty('volume', 1) 

log_file_path = "L:/SteamLibrary/steamapps/common/Counter-Strike Global Offensive/game/csgo/console.log" #location fo console.log(cs2 folder)
chat_pattern = re.compile(r'.*\[\w+\]\s*([^\:]+):\s*!say\s*(.*)')

def read_chat(chat_message):
    print(f"Chat message: {chat_message}")
    engine.say(chat_message)
    engine.runAndWait()

def monitor_log_file_polling():
    last_pos = 0 

    while True:
        try:
            with open(log_file_path, 'r', encoding='utf-8') as file:
                file.seek(last_pos) 
                new_lines = file.readlines() 
                last_pos = file.tell()

                if new_lines:
                    print(f"New lines detected: {new_lines}")

                for line in new_lines:
                    line = line.strip() 
                    print(f"Checking line: {line}")  
                    match = chat_pattern.match(line)
                    if match:
                        player_name = match.group(1)
                        chat_message = match.group(2)
                        
                        chat_message = replace_custom_words(chat_message, custom_words)
                        
                        full_message = f"{player_name} says: {chat_message}"
                        read_chat(full_message) 

        except KeyboardInterrupt:
            print("Exiting...")  
            break

if __name__ == "__main__":
    print("Monitoring CS2 chat messages...")
    monitor_log_file_polling()
