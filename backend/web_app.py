from flask import Flask, request, render_template, jsonify
from parser import StanfordNLP, format_pos, format_dep_parse
from encoder import Encoder, evaluate
from prepare import create_seq_mappings
import json

VOCAB_SIZE = 50002
NUM_UNITS = 100
BATCH_SIZE=64

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z]/'
encoder = Encoder(VOCAB_SIZE, NUM_UNITS, BATCH_SIZE)
encoder.load_weights('model/sc_model')

sNLP = StanfordNLP()

def read_file(file_name, read_json=False):
  data = []
  with open('Assets/' + file_name) as document:
    if read_json:
      data = json.load(document)
    else:
      data += ([str(x) for x in document.read().split()])
  return data

# Get vocabulary and dictionaries
word_vocab = read_file('word_vocab.txt')
word2id = read_file('word_dict.json', read_json=True)
pos2id = read_file('pos_dict.json', read_json=True)
dep2id = read_file('dep_dict.json', read_json=True)

# word dictionary
word_dict = read_file('word_dict.json', read_json=True)
inv_word_dict = {v: k for k, v in word_dict.items()}
inv_word_dict.update({0:'<delete>', 50001:'<unk>', 50002:'<unk>'})

# part of speech dictionary
pos_dict = read_file('pos_dict.json', read_json=True)
inv_pos_dict = {v: k for k, v in pos_dict.items()}
inv_pos_dict.update({0:'<delete>', 50001:'<unk>', 50002:'<unk>'})

# dependency dictionary
dep_dict = read_file('dep_dict.json', read_json=True)
inv_dep_dict = {v: k for k, v in dep_dict.items()}
inv_dep_dict.update({0:'<delete>', 50001:'<unk>', 50002:'<unk>'})

# word vocabulary
word_vocab = read_file('word_vocab.txt')


@app.route('/<sentence>')
def get_sentence(sentence):
    sentence = '<bos> ' + sentence + ' <eos>'
    ids = {
        'reg_words': sNLP.word_tokenize(sentence),
        'lower_words': sNLP.word_tokenize(sentence.lower()),
        'pos': format_pos(sNLP.pos(sentence.lower())),
        'dep': format_dep_parse(sNLP.dependency_parse(sentence.lower()))
    }
    words, pos, dep = create_seq_mappings([ids['lower_words']], [ids['pos']], [ids['dep']], word_vocab, word2id, pos2id, dep2id) 
    res = evaluate(encoder, words, pos, dep)
    results = []
    data = {}    
    for i in range(1, len(res[0])):
        keep = False
        word = ids['reg_words'][i]
        if res[0][int(i)]>.5 or i==len(res[0])-2:
            keep = True
        if word == '<eos>' or word == '<bos>':
            continue
        data[i] = {
                'word': word,
                'pos': inv_pos_dict[pos[0][i]],
                'dep': inv_dep_dict[dep[0][i]],
                'keep': keep
        }
    data = jsonify(data)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=80)
