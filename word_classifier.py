from typing import List

import numpy as np
import tensorflow as tf

from translator import Lang, translate


class WordClassifier:
    def __init__(self) -> None:
        self.n_letters = 8
        self.alphabet: tuple = Lang.ru_RU.value
        self.model = tf.keras.models.load_model('tf_models/word_classifier.hdf5')

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
        encoded_word = list(map(self.encode_char, word))
        filled_word = self.fill_encoded_word(encoded_word)
        return np.array(filled_word)

    def transform_words(self, words: List[str]) -> np.ndarray:
        return np.array([self.transform_word(x) for x in words])

    def encode_char(self, char: str) -> List[int]:
        encoded_char = [0] * len(self.alphabet)
        encoded_char[self.alphabet.index(char)] = 1
        return encoded_char

    def fill_encoded_word(self, encoded_word: List[List[int]]):
        fill_list = [[0] * len(self.alphabet) for _ in range(self.n_letters - len(encoded_word))]
        return encoded_word + fill_list
