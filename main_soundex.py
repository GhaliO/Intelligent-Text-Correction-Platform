import sys, os, re
sys.path.append('./')
import kenlm
import collections
import logging
from spelling_correcter_v2 import Spelling_Correcter as Spelling_Correcter_edits
from tools.data.get_soundex_code import Spelling_Correcter as Spelling_Correcter_sound
import time

arpa_path = 'data/lm_binary.arpa'
lm_model = kenlm.LanguageModel(arpa_path)

WORDS = []
with open('data/count.txt', 'r') as f:
    for line in f:
        word = line.strip()
        WORDS.append(word)

WORD_COUNTS = collections.Counter(WORDS)

soundex_code_dict = {}
with open('data/soundex_code.txt', 'r') as f:
    for line in f:
        soundex_code, words_info = line.strip().split(' ', 1)
        words_list = eval(words_info)
        soundex_code_dict[soundex_code] = words_list

Spell_C_edits = Spelling_Correcter_edits(WORD_COUNTS)
Spell_C_sound = Spelling_Correcter_sound(WORD_COUNTS, soundex_code_dict)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def correct_one(line):
    each_start_time = time.time()
    if ' ' in line.strip():
        utt, hpy = line.strip().split(' ', 1)
    else:
        utt = line.strip()
        hpy = ''
        return line.strip()
    hpy = re.sub(' +', ' ', hpy)
    words = hpy.strip().split(' ')
    for_time_start = time.time()
    for i in range(len(words)):
        #logging.info('words_num {}'.format(len(words)))
        each_for_time_start = time.time()
        word = words[i]
        ## 数字不调整
        #if word.isnumeric()
        #    continue

        # 'S 结尾不修改
        if len(word) >= 3 and word.endswith("'S"):
            continue

        if word.startswith("'"):
            candidates = list(Spell_C_edits.get_candidates(word))
        else:
            candidates = Spell_C_sound.get_candidates(word)
        #logging.info('get candidates time {} {} {} {}'.format(utt, word, len(candidates), time.time() - each_for_time_start))
        if len(candidates) == 1:
            words[i] = candidates[0]
        else:
            max_lm_score = float('-inf')
            for candidate in candidates:
                cand_start_time = time.time()
                if i == 0:
                    if len(words) == 1:
                        tmp_hpy = candidate
                    else:
                        tmp_hpy = ' '.join([candidate, words[i+1]])
                elif i + 1 < len(words):
                    tmp_hpy = ' '.join([words[i-1], candidate, words[i+1]])
                else:
                    tmp_hpy = ' '.join([words[i-1], candidate]) 
                cand_end_time = time.time()

                lm_score = lm_model.score(tmp_hpy.upper())
                #logging.info('{} {}'.format(candidate, lm_score))
                if lm_score > max_lm_score:
                    max_lm_score = lm_score
                    candidate_dict = {}
                    candidate_dict[str(candidate)] = lm_score
                lm_end_time = time.time()
                #logging.info('{} candidates_time: {}, lm_time: {}'.format(utt, cand_end_time-cand_start_time, lm_end_time-cand_end_time))
                    #print(tmp_hpy, lm_score)
            words[i] = list(candidate_dict.keys())[0]
        each_for_time_end = time.time()
        #logging.info('each_for_time {} {} {}'.format(utt, word, (each_for_time_end - each_for_time_start)))
    for_time_end = time.time()
    #logging.info('for_time {} {}'.format(utt, (for_time_end - for_time_start)))
    result = utt + ' ' + (' '.join(words)).upper()
    each_end_time = time.time()
    #logging.info('each_time {} {}'.format(utt, (each_end_time-each_start_time)))
    return result

if __name__ == '__main__':
    hpy_txt, hpy_fix_txt = sys.argv[1:3]

    start_time = time.time()
    count = ''
    with open(hpy_txt, 'r') as f:
        for line in f:
            #print(line.strip())
            hpy_fix = correct_one(line)
            count += hpy_fix + '\n'

    with open(hpy_fix_txt, 'w') as f:
        f.write(count)

    end_time = time.time()
    logging.info('total_time: {}'.format(end_time - start_time))
