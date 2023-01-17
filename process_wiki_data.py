import hanlp
import numpy as np
from itertools import chain
from tqdm import tqdm
from enum import IntEnum
from itertools import chain
import json
import argparse
import os
from multiprocessing import Pool, current_process

def split_para(text):
    return list(filter(None, text.split('\n')))

def to_4tag(text, split_sent, tok):
    full_split = list(chain(*split_sent(split_para(text))))
    for sentence in tok(full_split):
        for word in sentence:
            if len(word) == 1:
                yield (word, 'S', )
            else:
                yield (word[0], 'B', )
                for char in word[1:-1]:
                    yield (char, 'M', )
                yield (word[-1], 'E', )
        yield None

def get_texts_from_wiki_json_file(filename):
    texts = []
    file = open(filename, 'r')
    for line in file.readlines():
        texts.append(json.loads(line)['text'])
    return texts

def write_corpus_to(corpus, writable, pbar, split_sent, tok):
    for text in corpus:
        for item in to_4tag(text, split_sent, tok):
            if item is None:
                writable.write('SENTENCE END\n')
            else:
                writable.write('%s %s\n' % (item[0], item[1]))
        writable.write('TEXT END\n')
        pbar.update(1)

def process_task(filename, dest_filename):
    tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH, verbose=False)
    split_sent = hanlp.load(hanlp.pretrained.eos.UD_CTB_EOS_MUL, verbose=False)
    os.makedirs(os.path.dirname(dest_filename), exist_ok=True)
    corpus = get_texts_from_wiki_json_file(filename)
    # corpus = corpus[:3]
    current = current_process()
    with tqdm(total=len(corpus), desc=filename, leave=False, position=current._identity[0] - 1) as pbar:
        with open(dest_filename, 'w') as ofile:
            write_corpus_to(corpus, ofile, pbar, split_sent, tok)
    return dest_filename

def task_wrapper(task):
    return process_task(task[0], task[1])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    completed_list_file = os.path.join(args.output_dir, ".completed_list")
    completed_list = []
    if os.path.exists(completed_list_file):
        with open(completed_list_file) as f:
            completed_list = [l.strip() for l in f.readlines()]

    all_tasks = []
    for (dirpath, _, files) in os.walk(args.input_dir):
        for file in files:
            all_tasks.append((os.path.join(dirpath, file), os.path.join(args.output_dir, os.path.relpath(dirpath, args.input_dir), file), ))
    tasks = []
    for (ifile, ofile) in all_tasks:
        if ofile in completed_list:
            print('%s already completed, skipping ..' % ofile)
        tasks.append((ifile, ofile, ))
    print('Tasks:')
    for (ifile, ofile) in tasks:
        print('  %s --> %s' % (ifile, ofile))
    proceed = False
    while True:
        s = input('is this ok? [y/n] : ')
        if s == 'y':
            proceed = True
            break
        if s == 'n':
            proceed = False
            break

    if proceed:
        processes = os.cpu_count()
        with Pool(processes) as pool:
            with tqdm(total=len(tasks), desc='Total', leave=False, position=processes + 1) as pbar:
                for completed_file in pool.imap_unordered(task_wrapper, tasks):
                    with open(completed_list_file, 'a') as f:
                        f.write('%s\n' % completed_file)
                    pbar.update(1)

