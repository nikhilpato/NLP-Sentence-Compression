from flask import Flask, request, render_template, jsonify
from parser import StanfordNLP, format_pos, format_dep_parse
from encoder import VOCAB_SIZE, NUM_UNITS, BATCH_SIZE
from encoder import Encoder, evaluate
from prepare import create_seq_mappings
from utils import read_file


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z]/'

# Initialize Model
encoder = Encoder(VOCAB_SIZE, NUM_UNITS, BATCH_SIZE)
encoder.load_weights('model/sc_model')

# Initialize parser
sNLP = StanfordNLP()

# Get vocabulary and dictionaries
word_vocab = read_file('word_vocab.txt')
word2id = read_file('word_dict.json', read_json=True)
pos2id = read_file('pos_dict.json', read_json=True)
dep2id = read_file('dep_dict.json', read_json=True)

# word dictionary
word_dict = read_file('word_dict.json', read_json=True)
inv_word_dict = {v: k for k, v in word_dict.items()}
inv_word_dict.update({0:'<delete>', 50001:'<unk>', 50002:'<unk>'})

# word vocabulary
word_vocab = read_file('word_vocab.txt')


@app.route('/<sentence>')
def get_sentence(sentence):
    # add markers
    sentence = '<bos> ' + sentence + ' <eos>'
    # parse sentence
    ids = {
        'reg_words': sNLP.word_tokenize(sentence),
        'lower_words': sNLP.word_tokenize(sentence.lower()),
        'pos': format_pos(sNLP.pos(sentence.lower())),
        'dep': format_dep_parse(sNLP.dependency_parse(sentence.lower()))
    }
    # vectorize sequences
    words, pos, dep = create_seq_mappings([ids['lower_words']], [ids['pos']], [ids['dep']], word_vocab, word2id, pos2id, dep2id) 
    # get predictions
    res = evaluate(encoder, words, pos, dep)
    results = []
    data = {}    
    # create response by adding every word and simply indicating if its
    # kept or removed
    for i in range(1, len(res[0])):
        keep = False
        word = ids['reg_words'][i]
        # add period if not already added
        if res[0][int(i)]>.5 or i==len(res[0])-2:
            keep = True
        if word == '<eos>' or word == '<bos>':
            continue
        data[i] = {
                'word': word,
                'keep': keep
        }
    data = jsonify(data)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=80)
