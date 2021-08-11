import pyperclip
from typing import List
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import load_model
from tensorflow.python.framework.config import set_memory_growth
from tensorflow.config import list_physical_devices
import numpy as np
import keyboard
from time import sleep
import sys

physical_devices = list_physical_devices('GPU')
set_memory_growth(physical_devices[0], True)


class WordClassifier:
    def __init__(self) -> None:
        self.n_letters = 8  # words for model to classify are cut to specified length
        self.rus_letters = 'йцукенгшщзхъфывапролджэячсмитьбюё'
        eng_letters = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`'
        self.eng_to_rus_dict = {e: r for e,
                                r in zip(eng_letters, self.rus_letters)}
        # processes encoded words for classification
        self.model = load_model('./word_classifier.hdf5')
        self.char_encoder = OneHotEncoder()
        self.char_encoder.fit([[c] for c in self.rus_letters])

    def classify_words(self, words: List[str]):
        return np.argmax(self.model.predict(self.transform_words(words).reshape((-1, 33*self.n_letters))), axis=-1)

    def transform_word(self, word: str) -> np.ndarray:
        word = np.array(list(word)).reshape((-1, 1))
        return np.append(self.char_encoder.transform(word).toarray(), (np.zeros((self.n_letters, 33))), axis=0)[:self.n_letters]

    def transform_words(self, words: List[str]) -> np.ndarray:
        return np.array([self.transform_word(x) for x in words])


def change_language(classifier: WordClassifier):
    keyboard.release('ctrl')
    keyboard.release('alt')
    keyboard.release('k')

    # get selected text using copy
    keyboard.send('ctrl+c')
    sleep(0.1)
    s = pyperclip.paste().split()
    rus_letters = 'йцукенгшщзхъфывапролджэячсмитьбюё'
    eng_letters = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`'
    rus_to_eng_dict = {r: e for r, e in zip(rus_letters, eng_letters)}
    eng_to_rus_dict = {e: r for r, e in zip(rus_letters, eng_letters)}

    # removes symbols that can't be used in classification
    prepared_er_words = [''.join(
        [c if c in rus_letters or c in eng_letters else '' for c in x]) for x in s]
    prepared_r_words = [''.join(
        eng_to_rus_dict[c] if c in eng_letters else c for c in x) for x in prepared_er_words]

    classes = classifier.classify_words(prepared_r_words)

    # used for better text correction considering special symbols and uppercase
    ext_rus_letters = rus_letters + rus_letters.upper() + '.,"№;:?/'
    ext_eng_letters = eng_letters + \
        'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~/?@#$^&|'
    rus_to_eng_dict = {r: e for r, e in zip(ext_rus_letters, ext_eng_letters)}
    eng_to_rus_dict = {e: r for r, e in zip(ext_rus_letters, ext_eng_letters)}

    res_words = [''.join((eng_to_rus_dict[c] if c in ext_eng_letters else c) for c in x) if i else
                 ''.join((rus_to_eng_dict[c] if c in ext_rus_letters else c) for c in x) for i, x in zip(classes, s)]

    # yet can only correctly process one line texts. Transforms new lines into spaces otherwice
    new_s = ' '.join(res_words)
    sleep(0.1)
    pyperclip.copy(new_s)
    sleep(0.1)
    keyboard.send('ctrl+v')


if __name__ == '__main__':
    classifier = WordClassifier()
    hotkey = open('config.txt', 'r').read().strip().split(':')[1].strip()
    keyboard.add_hotkey(hotkey, change_language, args=(classifier,))
    keyboard.wait('esc')
