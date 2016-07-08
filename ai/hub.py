"""Central speech recognition code.

Requires: `pyaudio` and `SpeechRecongnition`
Run: `python hub.py`, say "Hey Matilda", then "<command>", e.g. "thank you"

"""
import os
import logging

import speech_recognition as sr

import commands as cmd
from config import COMMAND

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

# HELPERS ---------------------------------------------------------------------
def parse_commands(response):
    """Detect bot commands from an audio response."""
    # Using CB commands
    if response is not None and response.lower().startswith(COMMAND):
        response = "".join([u"!", response])
        # first_arg = message.split(" ")[0]
        # if first_arg.lower() == "hey {name}".format(name=NAME.lower()):
    return response

    # Only when given a CB command should it interact with the chat


# -----------------------------------------------------------------------------
# TODO: Replace
if __name__ == "__main__":
    # Microphone stays attentive unless told "Hey {name}... sleep"
    # `echo` and `feedback` are listen() objects
    with sr.Microphone() as source:
        print("Listening ...")

        while True:
            echo = listen(source)                          # listens passively
            logging.debug("echo: {}".format(echo))
            #print("echo: {}".format(echo))
            # Only response when called by name, e.g. "hey jarvis"
            # TODO: Need to stay in this block until satisfied; end after thank you
            if cmd.greet(echo):
                # Take new instructions here
                feedback = listen(source)                  # listens actively
                message = parse_commands(feedback)
                logging.debug("message: {}".format(message))
                print("""I heard: "{}" """.format(message))

                if cmd.sleep(feedback):
                    break

                #TODO: Clean up; automate command factory and inspection.
                cmd.chrome(feedback)
                cmd.jupyter(feedback)
                cmd.thanks(feedback)
                cmd.google(feedback)
