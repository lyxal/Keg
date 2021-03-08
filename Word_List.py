#!/usr/bin/env python
# -*- coding: utf-8 -*-
def generate_list():
    words = list()
    import os
    prepend = os.path.dirname(__file__) 
    source = open(prepend + "/docs/words.txt", encoding="utf-8").readlines()

    for word in source:
        if len(word) <= 3:
            continue
        if len(words) >= 61000:
            continue
        if word.startswith("#!comment:"):
            continue

        if all([x in "ABCDEFFGHIJKLMNOPQRSTUVWXYZ" for x in word]):
            continue
        
        words.append(word.strip("\n"))
    return words
