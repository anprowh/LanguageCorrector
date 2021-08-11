from time import sleep
from typing import List

import keyboard
import numpy as np
import pyperclip
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder

from translator import Lang, translate_list, translate


class WordClassifier:
    def __init__(self) -> None:
        self.n_letters = 8
        self.rus_letters = 'йцукенгшщзхъфывапролджэячсмитьбюё'
        eng_letters = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`'
        self.eng_to_rus_dict = {e: r for e,
                                         r in zip(eng_letters, self.rus_letters)}
        self.model = tf.keras.models.load_model('./word_classifier.hdf5')
        self.char_encoder = OneHotEncoder()
        self.char_encoder.fit([[c] for c in self.rus_letters])

    def prepare_word(self, word: str) -> str:
        alpha_word = "".join(filter(str.isalpha, word))
        short_word = alpha_word[:self.n_letters]
        lover_word = short_word.lower()
        rus_word = translate(lover_word, Lang.ru_RU)
        return rus_word

    def prepare_words(self, words: List[str]) -> List[str]:
        return list(map(self.prepare_word, words))

    def get_langs(self, words: List[str]) -> List[Lang]:
        words = self.prepare_words(words)
        return [Lang.ru_RU if num else Lang.en_US for num in self.classify_words(words)]

    def classify_words(self, words: List[str]):
        return np.argmax(self.model.predict(self.transform_words(words).reshape((-1, 33 * self.n_letters))), axis=-1)

    def transform_word(self, word: str) -> np.ndarray:
        word = np.array(list(word)).reshape((-1, 1))
        return np.append(self.char_encoder.transform(word).toarray(), (np.zeros((self.n_letters, 33))), axis=0)[
               :self.n_letters]

    def transform_words(self, words: List[str]) -> np.ndarray:
        return np.array([self.transform_word(x) for x in words])


def auto_translate(text: str, classifier: WordClassifier) -> str:
    words = text.split()
    langs_to = classifier.get_langs(words)
    return " ".join(translate_list(words, langs_to))


def change_language(classifier: WordClassifier):
    keyboard.release('ctrl')
    keyboard.release('alt')
    keyboard.release('k')
    keyboard.send('ctrl+c')
    sleep(0.1)
    s = pyperclip.paste().split()
    rus_letters = 'йцукенгшщзхъфывапролджэячсмитьбюё'
    eng_letters = 'qwertyuiop[]asdfghjkl;\'zxcvbnm,.`'
    rus_to_eng_dict = {r: e for r, e in zip(rus_letters, eng_letters)}
    eng_to_rus_dict = {e: r for r, e in zip(rus_letters, eng_letters)}

    prepared_er_words = [''.join(
        [c if c in rus_letters or c in eng_letters else '' for c in x]) for x in s]
    prepared_r_words = [''.join(
        eng_to_rus_dict[c] if c in eng_letters else c for c in x) for x in prepared_er_words]

    classes = classifier.classify_words(prepared_r_words)

    ext_rus_letters = rus_letters + rus_letters.upper() + '.,"№;:?/'
    ext_eng_letters = eng_letters + \
                      'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~/?@#$^&|'
    rus_to_eng_dict = {r: e for r, e in zip(ext_rus_letters, ext_eng_letters)}
    eng_to_rus_dict = {e: r for r, e in zip(ext_rus_letters, ext_eng_letters)}

    res_words = [''.join((eng_to_rus_dict[c] if c in ext_eng_letters else c) for c in x) if i else
                 ''.join((rus_to_eng_dict[c] if c in ext_rus_letters else c) for c in x) for i, x in zip(classes, s)]

    new_s = ' '.join(res_words)
    sleep(0.1)
    pyperclip.copy(new_s)
    sleep(0.1)
    keyboard.send('ctrl+v')


def main():
    pass


if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     classifier = WordClassifier()
#     hotkey = open('config.txt', 'r').read().strip().split(':')[1].strip()
#     keyboard.add_hotkey(hotkey, change_language, args=(classifier,))
#     keyboard.wait('esc')
