import re
import nltk
import numpy as np
import pandas as pd
from nltk import FreqDist

other_dep_annotations = {
    'obj': 'iobj',
    'cop': 'conj',
    'compound': 'nn',
    'nummod': 'num',
    'punct': 'p',
    'nmod': 'pobj',
    'npmod': 'npadvmod',
    'acl': 'npadvmod',
    'case': 'prep',
    'relcl': 'rel',
    'oprd': 'pred'
}


def create_seq_mappings(word_seq, pos_seq, dep_seq, vocabulary, word2id, pos2id, dep2id):
    """ For each of the given sequences, it maps their contents
        into their corresponding ids.
        
    Args:
        word_seq: A list of lists of words.
        pos_seq: A list of list of parts of speech.
        dep_seq: A list of list of dependency relations.
        vocabulary: The word vocabulary.
        word2id: The mapping from a word to an integer.
        pos2id: The mapping from a part of speech to an integer.
        dep2id: The mapping from a relation to an integer.
        
    Returns:
        word_seq_id: A list of sentences, where each of the words
            is mapped to a non-zero integer.
        pos_seq_id: A list of sentences, where each of the parts of 
            speeches is mapped to a non-zero integer.
        dep_seq_id: A list of sentences, where each of the relations
            is mapped to a non-zero integer.        
    
    """
    word_seq_id = []
    pos_seq_id = []
    dep_seq_id = []
    for sent_word, sent_pos, sent_dep in zip(word_seq, pos_seq, dep_seq):
        word_sent_id = []
        pos_sent_id = []
        dep_sent_id = []
        for word, pos, dep in zip(sent_word, sent_pos, sent_dep):
            if word in vocabulary:
                word_sent_id.append(word2id[word])
            else:
                word_sent_id.append(len(vocabulary)+1)
                
            pos_sent_id.append(pos2id[pos])

            # verify dependency annotation
            if dep in dep2id:
                dep_sent_id.append(dep2id[dep])
            elif dep in other_dep_annotations:
                correct_dep = other_dep_annotations[dep]
                dep_sent_id.append(dep2id[correct_dep])
            else:
                print(dep)
                dep_sent_id.append(dep2id['nn'])
            
        word_seq_id.append(word_sent_id)
        pos_seq_id.append(pos_sent_id)
        dep_seq_id.append(dep_sent_id)
    return word_seq_id, pos_seq_id, dep_seq_id
