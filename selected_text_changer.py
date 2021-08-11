from time import sleep

import keyboard
import pyperclip

from translator import translate_list
from word_classifier import WordClassifier


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
