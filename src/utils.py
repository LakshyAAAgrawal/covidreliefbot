import logging
import regex as re

def contains_iter(word_list, text, fuzzy=None, fuzzy_len=4):
    """
    fuzzy: string pattern of fuzzy behaviour
    """
    if not fuzzy:
        for i in re.finditer("(" + ")|(".join(word_list) + ")", text):
            yield i.group()
    else:
        for word in word_list:
            s = "(" + word + ")" + fuzzy if len(word) > fuzzy_len else word
            r = re.compile(s) # fuzzy is not None
            if re.search(r, text) is not None:
                yield word
