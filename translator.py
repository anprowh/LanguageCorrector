from enum import Enum
from typing import List


class Lang(Enum):
    en_US = frozenset('abcdefghijklmnopqrstuvwxyz')
    ru_RU = frozenset('абвгдеёжзийклмнопрстуфхцщшчъыьэюя')


keyboard_layouts = {
    Lang.ru_RU: tuple('ё1234567890-='
                      'йцукенгшщзхъ\\'
                      'фывапролджэ'
                      'ячсмитьбю.'
                      'Ё!"№;%:?*()_+'
                      'ЙЦУКЕНГШЩЗХЪ/'
                      'ФЫВАПРОЛДЖЭ'
                      'ЯЧСМИТЬБЮ,'),
    Lang.en_US: tuple('`1234567890-='
                      'qwertyuiop[]\\'
                      'asdfghjkl;\''
                      'zxcvbnm,./'
                      '~!@#$%^&*()_+'
                      'QWERTYUIOP{}|'
                      'ASDFGHJKL:"'
                      'ZXCVBNM<>?')
}

layout_translators = {
    (lang, lang_to): str.maketrans(dict(zip(keyboard_layouts[lang], keyboard_layouts[lang_to])))
    for lang in Lang
    for lang_to in Lang
}


def define_lang(word: str) -> Lang:
    word_set = set(word)
    for lang in Lang:
        if word_set & lang.value == word_set:
            return lang
    raise Exception(f"Can't recognize language of word \"{word}\"")


def translate(word: str, lang_to: Lang) -> str:
    return word.translate(layout_translators[define_lang(word), lang_to])


def translate_list(words: List[str], langs_to: List[Lang]) -> List[str]:
    return list(map(translate, words, langs_to))
