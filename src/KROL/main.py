import speech_recognition as sr
import cobra
import basket
import win32com.client as wincl
import pythoncom
import json
import os

# recognize speech using Wit.ai
SETTINGS_FILE = "settings.json"
SETTINGS_WIT_AI_KEY = "WitAIKey"  # Wit.ai keys are 32-character uppercase alphanumeric strings

def get_polish_speaker():
    pythoncom.CoInitialize()
    speaker = wincl.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    for voice in voices:
        desc = voice.GetDescription()
        #print("voice: id {} desc {}".format(voice.Id,voice.GetDescription()))
        if desc.find("Polish") >= 0:
            speaker.Voice = voice
            break
    return speaker

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE,"r") as f:
            settings = json.load(f)
            return settings
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE,"w") as f:
        json.dump(settings, f)

if __name__ == '__main__':
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    audio_source = sr.Microphone(sample_rate = 16000)
    with audio_source as source:
        # sometimes it may be better to adjust automatically for ambient noise, sometimes it's not
        #recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 1000 # adjust this to your value
    
    # read settings
    settings = load_settings()
    wit_ai_key = settings.get(SETTINGS_WIT_AI_KEY)
    if wit_ai_key == None:
        print("No wit.ai key found, please enter wit.ai key now:")
        wit_ai_key = input()
        settings[SETTINGS_WIT_AI_KEY] = wit_ai_key
        save_settings(settings)

    print("Say something!")

    cobra = cobra.Cobra(recognizer, audio_source, get_polish_speaker, basket.Basket(), wit_ai_key )
    cobra.daemon = True
    cobra.start()
    print("Cobra started, press ENTER to terminate")
    input()
    print("Requesting stop")
    cobra.stop()
    cobra.join()