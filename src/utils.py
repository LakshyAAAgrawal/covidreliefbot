import logging
import regex as re

def contains_iter(word_list, text):
    return re.finditer("(" + ")|(".join(word_list) + ")", text)

