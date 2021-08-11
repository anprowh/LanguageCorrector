from enum import Enum
from typing import Optional, List


class Lang(str, Enum):
    en_US = 'abcdefghijklmnopqrstuvwxyz'
    ru_RU = 'абвгдеёжзийклмнопрстуфхцщшчъыьэюя'


keyboard_layouts = {
    Lang.ru_RU: 'ё1234567890-=йцукенгшщзхъ\\фывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,',
    Lang.en_US: '`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
}


layout_translators = {
    (lang, lang_to): str.maketrans(keyboard_layouts[lang], keyboard_layouts[lang_to])
    for lang in Lang
    for lang_to in Lang
}


def define_lang(word: str) -> Optional[Lang]:
    lang: Lang
    for lang in Lang:
        if all(letter in lang for letter in word):
            return lang
    return None


def translate(word: str, lang_to: Lang):
    return word.translate(layout_translators[define_lang(word), lang_to])


def translate_list(words: List[str], langs_to: List[Lang]) -> List[str]:
    return list(map(lambda word, lang_to: translate(word, lang_to), words, langs_to))
