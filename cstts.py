import re
import pyttsx3
import json
import configparser

engine = pyttsx3.init()
config = configparser.ConfigParser()

config.read('settings.ini')

voices = engine.getProperty('voices')

config.get('General', 'path_console')
voice_set = config.get('Voice Settings', 'tts_voice')
speed_set = (config.get('Voice Settings', 'speed'))
volume_set = (config.get('Voice Settings', 'volume'))


def load_custom_words():
    try:
        with open('custom_words.json', 'r') as file:
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
for voice in voices:
    if voice.name == voice_set:
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', float(speed_set))
engine.setProperty('volume', float(volume_set))

log_file_path = config.get('General', 'path_console')

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
        except FileNotFoundError:
            print("console file not present or wrong folder")
            return
        
if __name__ == "__main__":
    print("Monitoring CS2 chat messages...")
    monitor_log_file_polling()
