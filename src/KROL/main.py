import speech_recognition as sr
import cobra
import basket
import win32com.client as wincl
import pythoncom

# recognize speech using Wit.ai
WIT_AI_KEY = "GCFLL32DWBYDD2DUW6FFJPHEPP53WWFT"  # Wit.ai keys are 32-character uppercase alphanumeric strings

def get_polish_speaker():
    pythoncom.CoInitialize()
    speaker = wincl.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    for voice in voices:
        desc = voice.GetDescription()
        print("voice: id {} desc {}".format(voice.Id,voice.GetDescription()))
        if desc.find("Polish") >= 0:
            speaker.Voice = voice
            break
    return speaker

if __name__ == '__main__':
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    audio_source = sr.Microphone(sample_rate = 16000)
    with audio_source as source:
        #recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = 1000
    
    print("Say something!")

    cobra = cobra.Cobra(recognizer, audio_source, get_polish_speaker, basket.Basket(), WIT_AI_KEY )
    cobra.daemon = True
    cobra.start()
    input()
    print("Requesting stop")
    cobra.stop()
    cobra.join()