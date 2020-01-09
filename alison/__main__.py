import scipy.io.wavfile as wav
import numpy as np
import sys
import argparse
import json
import logging
import threading
import subprocess
import os
import librosa as lib
import _thread
import respeaker
from pixel_ring import pixel_ring

from . import read_wav_file, listen, mic_listener
from . import learn_from_file, read_wav_file
from .recognition import SoundRecognizer
#from . import philips_hue as lamps
from .server import BluetoothServer
from . import respeaker_led as rl


def launch_bluetooth_server(mic_listener):
    bluetoothConServer = None

    def server_thread():
        bluetoothConServer.start()
        launch_bluetooth_server

    bluetoothConServer = BluetoothServer(mic_listener)
    thread1 = threading.Thread(target=server_thread)
    thread1.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        help="Recognize sound from an audio file instead of the ReSpeaker",
        type=str)
    parser.add_argument(
        "--mic",
        help="Use the computer microphone instead of the ReSpeaker",action='store_true')
    parser.add_argument(
        "--learn",
        help="Name of a file that holds all the learning data",
        type=str)
    parser.add_argument(
        "--dict", help="Use a precomputed dictionary.", type=str)
    parser.add_argument(
        "--save", help="Save a sample of dictionary and activation matrix", type=str)
    args = parser.parse_args()

    def kill_process(pid):
        res = os.popen("sudo kill -9 " + pid).read()
        #print("\n killed process [", pid, "] : res = [", res , "]\n")

    # Sink
    def callback(evt):
        print("Recognized", evt.tag, "at time", evt.time, "with value",
              evt.value)
        
        if (evt.tag =='phone_ring'):
            _thread.start_new_thread(rl.turn_on_led,(0,0,255))
        
        if (evt.tag =='sonnette'):
            _thread.start_new_thread(rl.turn_on_led,(255,0,0))

        if (evt.tag =="fire_alarm"):
            print("oui")
            _thread.start_new_thread(rl.turn_on_led,(0,255,0))

    recognizer = SoundRecognizer(callback=callback)

    # Dict
    if args.dict is not None:
        logging.info("Loading dictionary %s", args.dict)
        recognizer.load_dictionary(args.dict)
        recognizer.load_activations("samples/sample.act")

    # Learn
    if args.learn is not None:
        logging.info("Learn from file %s", args.learn)
        learn_from_file(recognizer, args.learn)

    # Source
    if args.file is not None:
        logging.info("Input signal set to file %s", args.file)
        rate, signal = read_wav_file(args.file)
        recognizer.process_audio(signal)

    # Save
    if args.save is not None:
        y, sample_rate = lib.load("samples/Fire_Alarm/fire_alarm1.wav")
        recognizer.add_dictionary_entry("fire", "")

        recognizer.save_activations("samples/sample.act")

    else:
        # Mic
        if args.mic:
            print("Input signal set to computer microphone")
            mic_listener = listen.MicListener(recognizer, True)
        else:
            print("Input signal set to ReSpeaker")
            mic_listener = listen.MicListener(recognizer, False)

        print("Starting bluetooth server thread")
        launch_bluetooth_server(mic_listener)

        mic_listener.run_listening()
