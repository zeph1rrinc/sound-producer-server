import json
import numpy as np

from os.path import join, dirname, abspath


class SpeakerRecognizer:
    def __init__(self):
        self.speakers = {}
        self.speakers_file_path = join(dirname(abspath(__file__)), "speakers.json")
        self.get_speakers()

    def get_speakers(self):
        try:
            with open(self.speakers_file_path, 'r') as file:
                self.speakers = json.load(file)
        except FileNotFoundError:
            open(self.speakers_file_path, 'w').close()

    def cosine_dist(self, x, y):
        nx = np.array(x)
        ny = np.array(y)
        return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

    def recognize(self, spk: list) -> str:
        max_dist = 1
        result = 'Unrecognized'
        for speaker in self.speakers.keys():
            spk = list(map(float, spk))
            dist = self.cosine_dist(self.speakers[speaker], spk)
            if dist < max_dist:
                max_dist = dist
                result = speaker
        return result

    def add_speaker(self, speaker_file: str):
        with open(speaker_file) as file:
            new_speaker = json.load(file)
        self.speakers[new_speaker['speaker']] = new_speaker['spk']
        with open(self.speakers_file_path, 'w') as file:
            json.dump(self.speakers, file, indent=4, ensure_ascii=False)
