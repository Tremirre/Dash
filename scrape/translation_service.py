import os

import yaml
import googletrans as gt

from pathlib import Path


class TranslationService:
    WORD_DICT_FILE = f"{Path(__file__).absolute().parent}\\wd.yaml"

    def __init__(self):
        self.translator = gt.Translator()
        self.words_dict = self.get_words_dict()

    def get_words_dict(self) -> dict:
        if not os.path.isfile(TranslationService.WORD_DICT_FILE):
            print("Word Dictionary not found!")
            return {}
        with open(TranslationService.WORD_DICT_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def export_words_dict(self, overwrite=True) -> None:
        if not overwrite and os.path.isfile(TranslationService.WORD_DICT_FILE):
            return
        with open(TranslationService.WORD_DICT_FILE, "w", encoding="utf-8") as f:
            yaml.dump(self.words_dict, f)

    def translate(self, text: str, src: str, dest: str) -> str:
        if not text or type(text) != str:
            return text
        if text in self.words_dict:
            return self.words_dict[text]
        translated = self.translator.translate(text, src=src, dest=dest)
        self.words_dict[text] = translated.text
        return translated.text
