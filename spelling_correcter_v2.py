# -*- coding: utf-8 -*-
import re
import functools

class Spelling_Correcter:
    def __init__(self, WORDS):
        self.WORDS = WORDS

    def known(self, words):
        """
        Return the subset of words that are actually 
        in our WORD_COUNTS dictionary.
        """
        return {w for w in words if w in self.WORDS}
    
    def edits0(self, word): 
        """
        Return all strings that are zero edits away 
        from the input word (i.e., the word itself).
        """
        return {word}
    
    @functools.lru_cache(maxsize=None)
    def edits1(self, word):
        """
        Return all strings that are one edit away 
        from the input word.
        """
        alphabet = ''.join([chr(ord('A')+i) for i in range(26)] + ["'"])
        def splits(word):
            """
            Return a list of all possible (first, rest) pairs 
            that the input word is made of.
            """
            return [(word[:i], word[i:]) 
                    for i in range(len(word)+1)]
                    
        pairs      = splits(word)
        deletes    = [a+b[1:]           for (a, b) in pairs if b]
        transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
        replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
        inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
        #print('replaces:', len(replaces), replaces)
        #print('deletes', len(deletes), deletes)
        #print('transposes', transposes)
        return set(deletes + transposes + replaces + inserts)
    
    @functools.lru_cache(maxsize=None)
    def edits2(self, word):
        """Return all strings that are two edits away 
        from the input word.
        """
        return {e2 for e1 in self.edits1(word) for e2 in self.edits1(e1)}
    
    def edits3(self, word):
        return {e3 for e1 in self.edits1(word) for e2 in self.edits1(e1) for e3 in self.edits1(e2) if len(e3) <= len(word) + 3}
        
    
    def get_candidates(self, word):
        word = word.upper()
        candidates =  (self.known(self.edits0(word)) or
                       self.known(self.edits1(word)) or
                       self.known(self.edits2(word)) or
                       {word})
        #print(len(edits1(word)))
        #print(len(edits2(word)))
        #print(len(known(edits2(word))))
        #return max(candidates, key=WORD_COUNTS.get)
        return candidates
    
    def correct_match(self, match):
        """
        Spell-correct word in match, 
        and preserve proper upper/lower/title case.
        """
        
        word = match.group()
        def case_of(text):
            """
            Return the case-function appropriate 
            for text: upper, lower, title, or just str.:
                """
            return (str.upper if text.isupper() else
                    str.lower if text.islower() else
                    str.title if text.istitle() else
                    str)
        return case_of(word)(self.correct(word.lower()))
        
    def correct_text_generic(self, text):
        """
        Correct all the words within a text, 
        returning the corrected text.
        """
        return re.sub('[a-zA-Z]+', self.correct_match, text)

if __name__ == '__main__':

    WORDS = []
    with open('data/count.txt', 'r') as f:
        for line in f:
            word = line.strip()
            WORDS.append(word.lower())
    
    sc = Spelling_Correcter(WORDS)

    original_word = 'fianlly'
    correct_word = sc.get_candidates(original_word)
    print('Original word:%s\nCorrect word:%s'%(original_word, correct_word))
#original_word = 'correcat'
#original_word = 'digitl'\
#original_word = 'firea'
#print('Original word:%s\nCorrect word:%s'%(original_word, correct_word))

   
   
