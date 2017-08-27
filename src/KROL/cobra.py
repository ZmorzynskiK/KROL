import threading
from enum import Enum
import speech_recognition as sr
import datetime
import winsound

class Cobra(threading.Thread):
    class RecognitionStep(Enum):
        HOT_WORD = 1,
        INTENT = 2

    def __init__(self, recognizer, audio_source, speaker_factory, basket, wit_ai_key, hot_word = "whisky charlie", 
                 hot_word_sens = 0.15, hot_word_time_limit = 2.5, intent_timeout = 2.0, intent_time_limit = 2.5,
                 intent_retries = 3):
        super().__init__()
        self._recognizer = recognizer
        self._audio_source = audio_source
        self._hot_word = hot_word
        self._hot_word_entries = [(hot_word, hot_word_sens)]
        self._hot_word_time_limit = hot_word_time_limit
        self._wit_ai_key = wit_ai_key
        self._intent_timeout = intent_timeout
        self._intent_time_limit = intent_time_limit
        self._speaker_factory = speaker_factory
        self._basket = basket
        self._intent_retries = intent_retries
        self._setup_intents()

    def _setup_intents(self):
        self._intents = {
            "poo_last_date_get": self._handle_get_last_poo,
            "poo_last_date_set": self._handle_set_last_poo,
            "eat_last_date_get": self._handle_get_last_eat,
            "eat_last_date_set": self._handle_set_last_eat,
            "sleep_last_date_get": self._handle_get_last_sleep,
            "sleep_last_date_set": self._handle_set_last_sleep
            }

    def run(self):
        self._step = Cobra.RecognitionStep.HOT_WORD
        self._stop_requested = False

        self._speaker = self._speaker_factory()
        self._speaker.Speak("Czekam na instrukcje")
        while self._stop_requested == False:
            # check the state we are at
            if self._step == Cobra.RecognitionStep.HOT_WORD:
                self._listen_hot_word()
            elif self._step == Cobra.RecognitionStep.INTENT:
                self._listen_intent()

    def stop(self):
        self._stop_requested = True

    def _listen_hot_word(self):
        with self._audio_source as s:
            try:
                audio = self._recognizer.listen(s, 0.5, self._hot_word_time_limit)
            except sr.WaitTimeoutError:  # listening timed out, just try again
                return
            
            if self._stop_requested:
                return

        #with open(datetime.datetime.now().strftime("%H_%M_%S.wav"), "wb") as f:
        #    f.write(audio.get_wav_data())
        try:
            res = self._recognizer.recognize_sphinx(audio,keyword_entries=self._hot_word_entries, show_all = False)
            #hyp = res.hyp()
            #if hyp is None:
            #    return
            #print("hyp {} | score {} | prob {}".format(hyp.hypstr, hyp.best_score, hyp.prob))
            #print ([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in res.seg()])
            res = res.strip()
            if res == self._hot_word:
                print("Hot word OK... go ahead!")
                # change state
                self._step = Cobra.RecognitionStep.INTENT
            else:
                print("?")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx request error; {0}".format(e))

    def _listen_intent(self):
        # get audio
        retry_nb = 0
        while retry_nb < self._intent_retries:
            winsound.PlaySound("SystemQuestion", winsound.SND_ASYNC)
            if retry_nb == 0:
                self._speaker.Speak("Tak, słucham?")
            else:
                self._speaker.Speak("Powiedz jeszcze raz")
            print("Say intent")        
            with self._audio_source as s:
                try:
                    audio = self._recognizer.listen(s, timeout = self._intent_timeout, phrase_time_limit = self._intent_time_limit)
                except sr.WaitTimeoutError:
                    print("No intent detected")
                    self._speaker.Speak("Co? Nie słyszę!")
                    retry_nb += 1
                    continue

            if self._stop_requested:
                return

            print("Intent got, recognizing...")
            self._speaker.Speak("Już, momencik")
            try:
                wit_res = self._recognizer.recognize_wit(audio, key=self._wit_ai_key, show_all = True)
                print("Wit.ai thinks you said " + str(wit_res))
                # get first entity
                if len(wit_res['entities']) > 0 and len(wit_res['entities']['intent']) > 0:
                    intent = wit_res['entities']['intent'][0]['value']
                    handler = self._intents.get(intent)
                    if handler == None:
                        print("Unhandled intent {}".format(intent))
                        self._speaker.Speak("Nie umiem udzielić odpowiedzi na to pytanie")
                    else:
                        handler()
                    break
                else:
                    self._speaker.Speak("Słyszę cię, ale nie rozumiem")
            except sr.UnknownValueError:
                print("Wit.ai could not understand audio")
                self._speaker.Speak("Nie wiem o co chodziło")
            except sr.RequestError as e:
                print("Could not request results from Wit.ai service; {0}".format(e))
                self._speaker.Speak("Nie zrozumiałam")

            retry_nb += 1


        # go back to hot word detection
        self._step = Cobra.RecognitionStep.HOT_WORD

    def _speak_timed(self, moment, short_ago_str, mid_ago_str, long_ago_str, long_ago_val):
        diff_secs = (datetime.datetime.now() - moment).total_seconds()
        diff_mins = diff_secs/60.0
        diff_hours = diff_mins/60.0
        if diff_hours > long_ago_val:
            self._speaker.Speak(long_ago_str)
        elif diff_hours <= 1:
            self._speaker.Speak(short_ago_str.format(diff_mins))
        else:
            self._speaker.Speak(mid_ago_str.format(diff_hours))

    def _handle_get_last_poo(self):
        last_poo = self._basket.get_last_poo_date()
        if last_poo == None:
            self._speaker.Speak("Nie wiem kiedy była ostatnia kupa")
        else:
            self._speak_timed(last_poo, "Ostatnia kupa była {:.0f} minut temu", "Ostatnia kupa była {:.1f} godziny temu",
                              "Ostatnia kupa była ponad 6 godzin temu, czyli dość dawno", 6 )
            
    def _handle_set_last_poo(self):
        self._basket.set_last_poo_date()
        self._speaker.Speak("Fiu fiu, śmierdząca sprawa, przyjęłam")

    def _handle_get_last_eat(self):
        last_eat = self._basket.get_last_eat_date()
        if last_eat == None:
            self._speaker.Speak("Nie wiem kiedy było ostatnie karmienie, zwyrodnialcy")
        else:
            self._speak_timed(last_eat, "Ostatnio zeżarło {:.0f} minut temu", "Ostatnio zeżarło {:.1f} godziny temu",
                              "Nie karmiliście dziecka od ponad 3 godzin, łajdaki", 3 )

    def _handle_set_last_eat(self):
        self._basket.set_last_eat_date()
        self._speaker.Speak("Doskonale, niech nam rośnie, przyjęłam")

    def _handle_get_last_sleep(self):
        last_eat = self._basket.get_last_sleep_date()
        if last_eat == None:
            self._speaker.Speak("Nie wiem kiedy ostatni raz spał")
        else:
            self._speak_timed(last_eat, "Ostatnio zasnął {:.0f} minut temu", "Ostatnio zasnął {:.1f} godziny temu",
                              "Jupi, śpi już od ponad 3 godzin", 3 )

    def _handle_set_last_sleep(self):
        self._basket.set_last_sleep_date()
        self._speaker.Speak("Doskonale, niech się wyśpi, przyjęłam")
            