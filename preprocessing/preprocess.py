import json
import sys

def preprocess_data(json_file_name, text_file_name, keep_word, keep_pos, keep_dep):
    """ Preprocess the Google sentence compression dataset.
        
        The flags indicate whether the word, the part of speech,
        or the word's dependency relation with its head word are 
        written into a text file.
        
        For all the options, the order of the sentence is
        maintained.
    
    Args:
        json_file_name: The name of the json file containing
            the sentence compression data.
        text_file: The name of the text file to write into.
        keep_word: A flag that indicates wheter a word should 
            be written.
        keep_pos: A flag that indicates whether a word's part 
            of speech should be written.
        keep_dep: A flag that indicates whether a word's 
            dependency relation with its head word should 
            be written.
            
    Returns:
        None
    
    """
    json_object = read_data(json_file_name)
    for sentence in json_object['sentences']:
        word_dict = create_word_dict(sentence)
        data = create_word_segments(sentence, word_dict)
        write_data(data, text_file_name, keep_word, keep_pos,keep_dep)


def generate_labels(json_file_name, text_file_name):
    """ For each sentence write the words of the compressed 
        sentence to a text file.
        
    Args:
        json_file_name: The name of the json file containing
            the sentence compression data.
        text_file: The name of the text file to write into.
        
    Returns:
        None
    
    """
    json_object = read_data(json_file_name)
    document = open(text_file_name, 'a')
    for sentence in json_object['sentences']:
        compressed = sentence['compression_untransformed']['text'][:-1]
        compressed = compressed + ' . \n'
        document.write(compressed)
    document.close()


def read_data(file_name):
    """ Read in the json file given.
    
    Args:
        file_name: The name of the json file containing
            the sentence compression data.
    
    Returns:
        data: The generated json object.
    """
    with open(file_name) as document:
        data = json.load(document)
    return data


def create_word_dict(sentence):
    """ Create a dictionary that contains every word in a 
        sentence with its corresponding part of speech.
        
    Args:
        sentence: An object generated from the 
            json file that contains the dependency
            tree of the sentence.
    Returns:
        word_dict: A dictionary that maps each word id
            to its corresponding word and part of speech.
    
    """
    word_dict = {}
    for node in sentence['source_tree']['node']:
        for word in node['word']:
            word_form = word['form']
            word_tag = word['tag']
            word_id = word['id']
            word_dict[word_id] = [word_form, word_tag]
    return word_dict


def create_word_segments(sentence, word_dict):
    """ For the given sentence, pair each word with its
        corresponding part of speech and its dependency
        reltion with its head word.
        
    Args:
        sentence: An object generated from the
            json file that contains the dependency
            tree for the sentence.
        word_dict: A dictionary that maps each word id
            to its corresponding word and part of speech.
    
    Returns:
        data: A list of pairings that contain the 
            word, its part of speech and its dependency
            relation with its head word.
    
    """
    data = []
    for element in sentence['source_tree']['edge']:
        child = word_dict[element['child_id']]
        dependency = element['label']
        data.append([child[0], child[1], dependency])
    return data


def write_data(data, file_name, keep_word, keep_pos, keep_dep):
    """ Write the data into a text file, conditioned on the 
        given flags.
    
    Args:
        data: A list of pairings that contain the 
            word, its part of speech and its dependency relation
            with its head word.
        file_name: The name of the text file.
        keep_word: A flag that indicates wheter a word should 
            be written.
        keep_pos: A flag that indicates whether a word's part 
            of speech should be written.
        keep_dep: A flag that indicates whether a word's 
            dependency relation with its head word should 
            be written.
            
    Returns:
        None
    
    """
    document = open(file_name, 'a')
    for word_segment in data:
        segment_string = ''
        if keep_word:
            segment_string += word_segment[0] + ' '
        if keep_pos:
            segment_string += word_segment[1] + ' '
        if keep_dep:
            segment_string += word_segment[2] + ' '
        document.write(segment_string)
        
    # One sentence per line
    document.write('\n')
    document.close()


if __name__ == '__main__':
    if sys.argv[1] == 'get_data':
#        pass
        json_file_name = sys.argv[2]
        text_file_name = sys.argv[3]
        keep_word = (sys.argv[4] == 'True')
        keep_pos = (sys.argv[5] == 'True')
        keep_dep = (sys.argv[6] == 'True')
        preprocess_data(json_file_name, text_file_name, keep_word, keep_pos, keep_dep)
    elif sys.argv[1] == 'get_labels':
        json_file_name = sys.argv[2]
        text_file_name = sys.argv[3]
        generate_labels(json_file_name, text_file_name)

        
     
    
