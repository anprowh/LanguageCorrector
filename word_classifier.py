from typing import List

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder

from translator import Lang, translate


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
