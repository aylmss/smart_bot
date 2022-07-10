from data import STOP_WORDS


def stop_logic(word):
    word=[x for x in word.split()]
    #print(word)
    if STOP_WORDS[0] in word or STOP_WORDS[1] in word or STOP_WORDS[2] in word:
        return True
    else:
        return False