from os import makedirs, remove
from os.path import exists, join
import wave
from time import time
import speech_recognition as speech_r
from loguru import logger


def save_file(size, stream):
    file_name = join('../temp', f'{time()}.wav')
    if not exists("../temp"):
        makedirs("../temp")
    sound_file = wave.open(file_name, 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(size)
    sound_file.setframerate(44100)
    sound_file.writeframes(stream)
    sound_file.close()
    return file_name


def recognize(size, stream, nickname):
    saved_file = save_file(int(size), stream)
    recogniser = speech_r.Recognizer()
    sample = speech_r.WavFile(saved_file)
    with sample as audio:
        content = recogniser.record(audio)
        recogniser.adjust_for_ambient_noise(audio)
        try:
            message = recogniser.recognize_google(content, language="ru-RU")
            logger.debug(f"Received new message from {nickname} - {message}")
        except speech_r.UnknownValueError:
            logger.error("Empty file!")
            return False
    remove(saved_file)
    return True
