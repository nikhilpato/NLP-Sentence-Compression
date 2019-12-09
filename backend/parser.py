from stanfordcorenlp import StanfordCoreNLP

class StanfordNLP:
    def __init__(self, host='http://18.188.143.217', port=9000):
        self.nlp = StanfordCoreNLP(host, port=port,
        timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
        self.props = {
        'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
        'pipelineLanguage': 'en',
        'outputFormat': 'json'
        }
    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)
    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)
    def ner(self, sentence):
        return self.nlp.ner(sentence)
    def parse(self, sentence):
        return self.nlp.parse(sentence)
    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)



def format_pos(pos_list):
    new_list = []
    for i in pos_list:
        new_list.append(i[1])
    return new_list

def format_dep_parse(parse_list):
    parse_list.sort(key=lambda tup: tup[2])
    new_list = []
    for i in parse_list:
        new_list.append(i[0])
    return new_list



if __name__ == '__main__':
    sNLP = StanfordNLP()
    text = 'parrots do not swim'
    print("POS:", format_pos(sNLP.pos(text)))
    print("Tokens:", sNLP.word_tokenize(text))
    print("Dep Parse:", format_dep_parse(sNLP.dependency_parse(text)))