"""Central speech recognition code.

Requires: `pyaudio` and `SpeechRecongnition` (virtual environment recommended)
Run: `python matilda.py`, say "Hey Matilda", then "<command>", e.g. "thank you"

"""
import os
import sys
import logging
import asyncio

import speech_recognition as sr

from . import commands as cmd


# INPUT -----------------------------------------------------------------------
async def listen_nonthreaded(device, source):
    """Return a non-threaded PyAudio object; default."""
    device.adjust_for_ambient_noise(source)                # auto sets threshold
    audio = device.listen(source)
    return audio


async def listen_threaded(device, source, loop):
    """Return a threaded, PyAudio, Future object; an async context manager sub."""
    import threading
    result_future = asyncio.Future()
    def threaded_listen():
        with source as s:
            try:
                audio = device.listen(s)
                loop.call_soon_threadsafe(result_future.set_result, audio)
            except Exception as e:
                loop.call_soon_threadsafe(result_future.set_exception, e)
    listener_thread = threading.Thread(target=threaded_listen)
    listener_thread.daemon = True
    listener_thread.start()
    return await result_future


async def handle_audio(device, audio):
    """Return a str response from the AI backend, given a PyAudio object."""
    try:
        # AI Backends
        #return recog.recognize_sphinx(audio)
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        return device.recognize_google(audio)              # default AI
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

async def get_audio(device, source, threaded):
    """Return a handled audio request."""
    if threaded:
        loop = asyncio.get_event_loop()
        audio = await listen_threaded(device, source, loop)
    else:
        audio = await listen_nonthreaded(device, source)

    return await handle_audio(device, audio)

# MAIN ------------------------------------------------------------------------
async def main(device, source, threaded=False):
    """Main loops for passive and active listening."""
    while True:
        passive_echo = await get_audio(device, source, threaded=threaded)
        logging.debug("echo: {}".format(passive_echo))
        print("echo: {}".format(passive_echo))
        # Only response when called by name, e.g. greetring = "hey jarvis"
        # Re-enter passive mode bye saying "<greeting>, switch off"
        if cmd.greet(passive_echo):
            while True:
                # Take new instructions here
                active_echo = await get_audio(device, source, threaded=threaded)
                message = cmd.parse_commands(active_echo)
                logging.debug("message: {}".format(message))
                print("""I heard: "{}" """.format(message))

                if cmd.thanks(active_echo):
                    print("Listening ...")
                    break

                if cmd.off(active_echo):
                    sys.exit("Shutting down ...")

                #TODO: Clean up; automate command factory and inspection.
                cmd.chrome(active_echo)
                cmd.editor(active_echo)
                cmd.jupyter(active_echo)
                cmd.thanks(active_echo)
                # BUG: hangs with google search
                cmd.search(active_echo)


# Non-threaded example
async def run(use_threads=False):
    """Use a simple context manager for the microphone."""
    recognizer = sr.Recognizer()
    #recog.energy_threshold = 2000                         # range 50 to 4000 is good
    if use_threads:
        # Simulate an async context manager using threads.
        # https://github.com/Uberi/speech_recognition/issues/137
        print("Using threads.  Listening ...")
        source = sr.Microphone()
        await main(recognizer, source, threaded=use_threads)
    else:
        # Use a simple context manaaer for the microphone.
        with sr.Microphone() as source:
            # FIX: intial hesitation when mic starts
            print("Listening ...")
            await main(recognizer, source, threaded=use_threads)

# For testing; overrrides catcus event-loop
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run(True))
