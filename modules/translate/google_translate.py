#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from googletrans import Translator
import time


# text = 'farming'
# lang = 'am'
# translated = 'እርሻ'

def translateText(text, lang_code):
    translator = Translator()
    translator_results = translator.translate(text, dest=lang_code)
    text_translated_ascii = translator_results.text
    text_translated_utf8 = text_translated_ascii.encode('utf8')
    text_translated_ascii = str(translator_results.text)
    time.sleep(2)
    return text_translated_ascii


def detectLang(string):
    translator = Translator()
    result = translator.detect(string)
    result = format(result)
    result = result[14:16]
    time.sleep(2)
    return result


    # translated = translateText(text, lang)
    # print(translated)

    # l = detectLang(translated)
    # print(l)
