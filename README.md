# New-words-machine
Python program to help learn new words in languages. You can either choose to use words from a txt file (Faster) or by randomizing them. Program works by selecting a chosen amount of words in english, and then translating them to the chosen languages. 

Program uses two languages by default. This is because i do not fully trust the translation program and would rather have a way to double check.


Randomizer fetches words from:
https://random-word-api.herokuapp.com/word

Word txt files is included. File contains the 3000 most common words in the english language. Files with more words can be found in for example:
https://github.com/dwyl/english-words

Packages and tools required:
tkinter
random
os
requests
deep_translator
