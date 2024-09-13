import sys, os
import multiprocessing
sys.path.append('tools/decode')
#from compute-wer import Calculator
Instrument_Control = __import__("compute-wer")
Calculator = getattr(Instrument_Control, "Calculator")
characterize = getattr(Instrument_Control, "characterize")

def get_each_wer(result):
    key, lab, rec = result
    calculator = Calculator()

    lab = characterize(lab)
    rec = characterize(rec)
    result = calculator.calculate(lab, rec)
    #print(lab, rec, result)
    if result['all'] != 0 :
        wer = float(result['ins'] + result['sub'] + result['del']) * 100.0 / result['all']
    else:
        wer = 0.0
    return key, wer

if __name__ == '__main__':
    ref_txt, hpy_txt, hpy_fix_txt, worse_txt = sys.argv[1:5]

    ref_dict = {}
    with open(ref_txt, 'r') as f:
        for line in f:
            if len(line.strip().split(' ')) >= 2:
                id, ref = line.strip().split(' ', 1)
            else:
                id = line.strip()
                ref = ''
            ref_dict[id] = ref

    hpy_dict = {}
    with open(hpy_txt, 'r', errors = 'ignore') as f:
        for line in f:
            if len(line.strip().split(' ')) >= 2:
                id, hpy = line.strip().split(' ', 1)
            else:
                id = line.strip()
                hpy = ''
            hpy_dict[id] = hpy

    hpy_fix_dict = {}
    with open(hpy_fix_txt, 'r', errors = 'ignore') as f:
        for line in f:
            if len(line.strip().split(' ')) >= 2:
                id, hpy = line.strip().split(' ', 1)
            else:
                id = line.strip()
                hpy = ''
            hpy_fix_dict[id] = hpy

    resuts_list = []
    for key in hpy_dict.keys() & ref_dict.keys():
        resuts_list.append([key, ref_dict[key], hpy_dict[key]])

    hpy_wer_dict = {}
    for result in resuts_list:
        key, wer = get_each_wer(result)
        hpy_wer_dict[key] = wer

    resuts_list = []
    for key in hpy_fix_dict.keys() & ref_dict.keys():
        resuts_list.append([key, ref_dict[key], hpy_fix_dict[key]])

    hpy_fix_wer_dict = {}
    for result in resuts_list:
        key, wer = get_each_wer(result)
        hpy_fix_wer_dict[key] = wer

    count = ''
    for key in hpy_wer_dict.keys() & hpy_fix_wer_dict.keys():
        hpy_wer = hpy_wer_dict[key]
        hpy_fix_wer = hpy_fix_wer_dict[key]
        if hpy_fix_wer > hpy_wer:
            count += key + '\n'

    with open(worse_txt, 'w') as f:
        f.write(count)

