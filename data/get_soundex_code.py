import sys, os

def soundex(word):
    # Step 1: 将名字转换成大写，并将第一个字母保留下来
    word = word.upper()
    soundex_code = word[0]
    
    # Step 2: 将其他字母用数字代替
    for char in word[1:]:
        if char in ['B', 'F', 'P', 'V']:
            soundex_code += '1'
        elif char in ['C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']:
            soundex_code += '2'
        elif char in ['D', 'T']:
            soundex_code += '3'
        elif char == 'L':
            soundex_code += '4'
        elif char in ['M', 'N']:
            soundex_code += '5'
        elif char == 'R':
            soundex_code += '6'
    
    # Step 3: 删除连续出现的相同数字
    soundex_code = soundex_code[0] + ''.join([soundex_code[i] for i in range(1, len(soundex_code)) if soundex_code[i] != soundex_code[i-1]])
    
    # Step 4: 删除数字 0，并将编码补足到 4 个数字
    soundex_code = soundex_code.replace('0', '')
    soundex_code = soundex_code.ljust(4, '0')
    
    return soundex_code
    
class Spelling_Correcter:
    def __init__(self, WORDS, soundex_code_dict):
        self.WORDS = WORDS
        self.soundex_code_dict = soundex_code_dict

    def get_candidates(self, word):
        if word.upper() in self.WORDS:
            return [word]
        soundex_code = soundex(word)
        soundex_code_sub = soundex_code[:4]
        word_len = len(word)
        candidates = []
        if soundex_code_sub in self.soundex_code_dict:
            #return self.soundex_code_dict[soundex_code_sub]
            for candidate in self.soundex_code_dict[soundex_code_sub]:
                if abs(len(candidate) - len(word)) <= 3:
                    candidates.append(candidate)
            if len(candidates) > 0:
                return candidates
            else:
                return [word]
        else:
            return [word]


if __name__ == '__main__':

    #word = "AARDVARK"
    #soundex_code = soundex(word)
    #soundex_code_sub = soundex_code[:4]

    soundex_code_dict = {}
    with open('data/count.txt', 'r') as f:
        for line in f:
            word = line.strip()
            soundex_code = soundex(word)
            soundex_code_sub = soundex_code[:4]
            if soundex_code_sub in soundex_code_dict:
                soundex_code_dict[soundex_code_sub].append(word)
            else:
                soundex_code_dict[soundex_code_sub] = [word]

    count = ''
    for key, value in soundex_code_dict.items():
        count += key + ' ' + str(value) + '\n'

    with open('data/soundex_code.txt', 'w') as f:
        f.write(count)
