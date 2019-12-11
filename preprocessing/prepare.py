import re
import nltk
import numpy as np
import pandas as pd
from nltk import FreqDist
import preprocess

def prepare_data(word_file_name, pos_file_name, dep_file_name, labels_file_name):
    """ Converts the data into appropriate input
        sequences.
        
    Args:
        word_file_name: The name of the text file containing the words.
        pos_file_name: The name of the text file containing the parts 
            of speeches for each word.
        dep_file_name: The name of the text file containing the 
            dependency relation between each word and its head word.
        labels_file_name: The text file with the correct sentence
            compressions.
            
    Returns:
        word_seq_id: A list of sentences, where each of the words
            is mapped to a non-zero integer.
        pos_seq_id: A list of sentences, where each of the parts of 
            speeches is mapped to a non-zero integer.
        dep_seq_id: A list of sentences, where each of the relations
            is mapped to a non-zero integer.
        word2id: A dictionary that contains the mapppings for each
            word.
        pos2id: A dictionary that contains the mappings for each of 
            the parts of speeches.
        dep2id: A dictionary that contains the mappings for each 
            of the relations.
        word_vocab: The word vocabulary.
    
    """
    word_seq = read_file(word_file_name, to_lower=True, replace_int=True)
    pos_seq = read_file(pos_file_name)
    dep_seq = read_file(dep_file_name)
    if not verify_dimensions(word_seq, pos_seq, dep_seq):
        return False
    word_vocab, pos_vocab, dep_vocab = create_vocabulary(word_seq, pos_seq, dep_seq)
    word2id = create_mapping(word_vocab)
    pos2id = create_mapping(pos_vocab)
    dep2id = create_mapping(dep_vocab)
    word_seq_id, pos_seq_id, dep_seq_id = create_seq_mappings(
        word_seq, 
        pos_seq, 
        dep_seq, 
        word_vocab,
        word2id, 
        pos2id, 
        dep2id
    )
    return word_seq_id, \
           pos_seq_id, \
           dep_seq_id, \
           word2id, \
           pos2id, \
           dep2id, \
           word_vocab


def read_file(file_name, to_lower=False, replace_int=False):
    """ Tokenizes each sentence in the file.
    
    Args:
        file_name: The name of the text file with
            sentences.
        to_lower: Indicates whether the tokens should
            be converted to lowercase.
        replace_int: Indicates whether tokens containg
            number should be replace by '##'
            
    Returns:
        lines: A list of tokenized sentences.
        
    """
    lines = []
    with open(file_name) as document:
        for line_num, line in enumerate(document):
            sentence = line.replace('\n', '<eos>')
            sentence = '<bos> ' + sentence
            if to_lower:
                sentence = sentence.lower()
            if replace_int:
                sentence = re.sub(r'\S*\d+\S*', '##', sentence)
            lines.append(sentence.split())
    return lines


def verify_dimensions(word_seq, pos_seq, dep_seq):
    """ Verifies that all the sequences have the same
        dimensions.
        
    Args:
        word_seq: A list of lists of words.
        pos_seq: A list of list of parts of speech.
        dep_seq: A list of list of dependency relations.
            
    Returns:
        Boolean.
        
    """
    for sent_word, sent_pos, sent_dep in zip(word_seq, pos_seq, dep_seq):
        if (
            len(sent_word) != len(sent_dep)
            or len(sent_word) != len(sent_pos)
            or len(sent_dep) != len(sent_pos)):
            return False
    return True  


def create_mapping(seq):
    """ Creates the mappings from a token to a 
        non-zero integer.
        
    Args:
        seq: A list of list of elements.
    
    Returns:
        seq2id: A dictionary that contains mappings
            from words to ids.
    
    """
    seq2id = {}
    for token_id, token in enumerate(seq):
        seq2id[token] = token_id+1
    return seq2id


def create_vocabulary(word_seq, pos_seq, dep_seq):
    """ Creates the word vocabulary.
    
    Args:
        word_seq: A list of lists of words.
        pos_seq: A list of list of parts of speech.
        dep_seq: A list of list of dependency relations.
        
    Returns:
        word_vocab: The word vocabulary.
        pos_vocab: The part of speech vocabulary.
        dep_vocab: The dependency relation vocabulary.
        
    """
    bag_of_words = []
    pos_vocab = set()
    dep_vocab = set()
    for sent_word, sent_pos, sent_dep in zip(word_seq, pos_seq, dep_seq):
        for word, pos, dep in zip(sent_word, sent_pos, sent_dep):
            bag_of_words.append(word)
            pos_vocab.add(pos)
            dep_vocab.add(dep)
    freq_words = FreqDist(bag_of_words)
    word_vocab = [pair[0] for pair in freq_words.most_common(50000)]   
    return word_vocab, pos_vocab, dep_vocab


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
            dep_sent_id.append(dep2id[dep])
            
        word_seq_id.append(word_sent_id)
        pos_seq_id.append(pos_sent_id)
        dep_seq_id.append(dep_sent_id)
    return word_seq_id, pos_seq_id, dep_seq_id


def create_target_mapping(json_file_names, word_file_name, labels_file_name, word2id, vocabulary):
    """ Create the target sequence mappings. In order to map the target sequence
        to the orginal sequence the tree ids from the json files are needed ot 
        know which words were kept and which were removed.
        
    Args:
        json_file_names: A list of json files that contain the data.
        word_file_name: The name of the text file containing the words.
        labels_file_name: The text file with the correct sentence compressions.
        word2id: The mapping from a word to an integer.
        vocabulary: The word vocabulary.
        
    Returns:
        target_seq_id: A list of sentences, where each of the words
            is mapped to an integer. It has the same dimesionality 
            of word_seq_id. A zero indicates that the word has been
            removed in the compression.
    """
    target_seq_id = []
    target_seq = read_file(labels_file_name, to_lower=True, replace_int=True)
    word_seq = read_file(word_file_name, to_lower=True, replace_int=True)
    sent_index = 0
    
    # Iterate files
    for file_name in json_file_names:
        json_object = preprocess.read_data(file_name)
        
        # Iterate sentences in a file
        for sentence in json_object['sentences']:
            word_dict = preprocess.create_word_dict(sentence)
            # Skip ('ROOT ') entry at [0]
            sent_word_ids = list(word_dict.keys())[1:]
            compression_word_ids = get_compression_word_ids(
                sentence['compression_untransformed'])
            # Vocabulary only has preprocessed words not the original words
            preprocessed_sent = word_seq[sent_index]
            target_sent_id = []
            # Append <bos> id
            target_sent_id.append(word2id[preprocessed_sent[0]])
            word_index = 1

            # Iterate words in a sentence
            # Preprocessed sentence may be shorter than original.
            # The preprocessed sentence contains <bos> and <eos>
            # Iterate until one word before <eos> which should be ('.'), 
            # reduce length by 3
            # Skip last entry ('.') and add until the end
            for word_id in sent_word_ids[:len(preprocessed_sent)-3]:
                word = preprocessed_sent[word_index]
                if word_id in compression_word_ids:
                    if word in vocabulary:
                        target_sent_id.append(word2id[word])
                    else:
                        target_sent_id.append(len(vocabulary)+1)
                else:
                    target_sent_id.append(0)
                word_index += 1

            # Append ('.') id, its in the word ids but not in compressed ids
            # It may not be a ('.'), first check to make sure
            if preprocessed_sent[-2] in vocabulary:
                target_sent_id.append(word2id[preprocessed_sent[-2]])
            else:
                target_sent_id.append(len(vocabulary)+1)
            # Append <eos> id
            target_sent_id.append(word2id[preprocessed_sent[-1]]) 
            target_seq_id.append(target_sent_id)
            sent_index += 1
            
    return target_seq_id


def get_compression_word_ids(json_object_compression):
    """ Get the word ids of the words that are kept in 
        the compression.
        
    Args:
        json_object_compression: The compression sub object 
            in the original json file.
            
    Returns:
        word_ids: The ids of the words that are kept in the 
            compression.
    
    """
    word_ids = []
    compression_edges = json_object_compression['edge']
    for edge in compression_edges:
        word_ids.append(edge['child_id'])
    return word_ids
