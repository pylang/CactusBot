"""Central speech recognition code.

Requires: `pyaudio` and `SpeechRecongnition` (virtual environment recommended)
Run: `python matilda.py`, say "Hey Matilda", then "<command>", e.g. "thank you"

"""
import os
import sys
import logging

import speech_recognition as sr

import commands as cmd


# INPUT -----------------------------------------------------------------------
recog = sr.Recognizer()
#recog.energy_threshold = 2000                             # Range 50 to 4000 is good

def listen(source):
    """Return a str response from the AI backend."""
    recog.adjust_for_ambient_noise(source)                 # auto sets threshold
    audio = recog.listen(source)

    try:
        # AI Backends
        #return recog.recognize_sphinx(audio)
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        return recog.recognize_google(audio)               # default AI
        # return recog.recognize_wit(audio)
        # return recog.recognize_bing(audio)
        # return recog.recognize_api(audio)
        # return recog.recognize_ibm(audio)
    except sr.UnknownValueError:
        print("Pardon.  I could not understand the audio.")
    except sr.RequestError as e:
        print("Recognition Error: {0}".format(e))
    else:
        return ""

# -----------------------------------------------------------------------------
#     # Microphone stays attentive unless told "Hey {name}... sleep"
#     # `echo` and `feedback` are listen() objects
with sr.Microphone() as source:
    # FIX: intial hesitation when mic starts
    print("Listening ...")

    while True:
        echo = listen(source)                          # listens passively
        logging.debug("echo: {}".format(echo))
        print("echo: {}".format(echo))
        # Only response when called by name, e.g. "hey jarvis"
        # TODO: Need to stay in this block until satisfied; end after thank you
        if cmd.greet(echo):
            while True:
                # Take new instructions here
                feedback = listen(source)                  # listens actively
                message = cmd.parse_commands(feedback)
                logging.debug("message: {}".format(message))
                print("""I heard: "{}" """.format(message))

                if cmd.thanks(feedback):
                    print("Listening ...")
                    break

                if cmd.off(feedback):
                    sys.exit("Shutting down ...")


                #TODO: Clean up; automate command factory and inspection.
                cmd.chrome(feedback)
                cmd.editor(feedback)
                cmd.jupyter(feedback)
                cmd.thanks(feedback)
                # BUG: hangs with google search
                cmd.search(feedback)
