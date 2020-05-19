#!/usr/bin/env python
# coding=utf-8

import sys
import Levenshtein

def phoneme_error_rate(p_seq1, p_seq2):
    """Source: https://fehiepsi.github.io/blog/grapheme-to-phoneme/"""
    p_vocab = set(p_seq1 + p_seq2)
    p2c = dict(zip(p_vocab, range(len(p_vocab))))
    c_seq1 = [chr(p2c[p]) for p in p_seq1]
    c_seq2 = [chr(p2c[p]) for p in p_seq2]
    return Levenshtein.distance(''.join(c_seq1),
                                ''.join(c_seq2)) / len(c_seq2)

def print_stats(test, gold):
    if not len(test) == len(gold):
        sys.exit('test and gold file do not have the same length')
    total = len(test)
    test_per = 0
    test_wer = 0
    for n, item in enumerate(test):
        testtrans = item.strip().split('\t')[1].split(' ')
        goldtrans = gold[n].strip().split('\t')[1].split(' ')
        per = phoneme_error_rate(testtrans, goldtrans)
        wer = int(testtrans != goldtrans)
        test_per += per
        test_wer += wer
    test_per = test_per / total * 100
    test_wer = test_wer / total * 100
    print(f'WER: {test_wer}\nPER: {test_per}')


if __name__ == "__main__": 
    try:
        goldfile = sys.argv[1]
        testfile = sys.argv[2]
    except IndexError:
        exit('Please provide filepath')
    
    with open(goldfile, 'r') as gf, open(testfile, 'r') as tf:
        goldlines = gf.readlines()
        testlines = tf.readlines()

        print_stats(testlines, goldlines)