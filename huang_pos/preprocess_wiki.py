############################
### INITIALIZE VARIABLES ###
############################

# see https://spacy.io/api/annotation#pos-tagging for description of POS

POS_DICT = {
    'NOUN': 0,
    'VERB': 1,
    'ADJ': 2,
    'ADV': 3,
    'DET': 4,
    'CONJ': 5,
    'NUM': 6,
    'ADP': 7,
    'PROPN': 8,
    'PART': 9,
    'SPACE': 10,
    'INTJ': 11,
    'PRON': 12,
    'SYM': 14,
    'X': 15
}

WORD_ID = 'word_id'
FREQUENCY = 'frequency'
NUM_DOCS = 'num_docs'
SEEN_IN_DOC = 'seen_in_doc'
LAST_WORD_ID = 2 # 0, 1 and 2 used for eof, beginning padding and end padding
OTHER_POS = set()

# the n-th value of df_vals is the number of documents that contain the word with id n-1
df_vals = []

# a set of all the words (e.g. duck, run, etc.). used to look up if a new word_id should be created
words = set()

# vocab words mapped to their [word_id, frequency, num_docs, seen_in_doc] in the corpus. each vocab word is the originalword_pos (e.g. duck_noun and duck_verb)
# word_id is a string formatted as
vocab = dict()

EOD = 'eeeoddd_x'
BEG_PAD = '<s>_x'
END_PAD = '</s>_x'
WIKI_EOD = "---END.OF.DOCUMENT---"
TOTAL_DOCS = 0

import collections
vocab = collections.OrderedDict()
vocab[EOD] = {
    WORD_ID:'1_x',
    FREQUENCY: 0,
    NUM_DOCS: 0,
    SEEN_IN_DOC: False
}
vocab[BEG_PAD] = {
    WORD_ID:'2_x',
    FREQUENCY: 0,
    NUM_DOCS: 0,
    SEEN_IN_DOC: False
}
vocab[END_PAD] = {
    WORD_ID:'3_x',
    FREQUENCY: 0,
    NUM_DOCS: 0,
    SEEN_IN_DOC: False
}

########################
### HELPER FUNCTIONS ###
########################


def write_to_file(fn, data):
    with open(fn, 'a') as mfile:
        mfile.write(data + '\n')

def set_up_word(text, pos, vocab):
    global LAST_WORD_ID, WORD_ID, POS_DICT, FREQUENCY, NUM_DOCS, SEEN_IN_DOC, TOTAL_DOCS
    # TODO: why are some pos not in POS_DICT
    if pos in POS_DICT:
        LAST_WORD_ID += 1
        vocab[word] = dict()
        word_dict = vocab[word]
        word_dict[WORD_ID] = str(LAST_WORD_ID) + "_" + str(POS_DICT[pos])
        word_dict[FREQUENCY] = 1
        word_dict[NUM_DOCS] = 1
        word_dict[SEEN_IN_DOC] = True
        return word_dict[WORD_ID]
    else:
        OTHER_POS.add(pos)
        return None

def update_word(text, pos, vocab):
    global LAST_WORD_ID, WORD_ID, POS_DICT, FREQUENCY, NUM_DOCS, SEEN_IN_DOC, TOTAL_DOCS
    word_dict = vocab[word]
    word_dict[FREQUENCY] += 1
    if not word_dict[SEEN_IN_DOC]:
        word_dict[NUM_DOCS] += 1
        word_dict[SEEN_IN_DOC] = True
    return word_dict[WORD_ID]

def update_eod(words_in_doc):
    global LAST_WORD_ID, WORD_ID, POS_DICT, FREQUENCY, NUM_DOCS, SEEN_IN_DOC, TOTAL_DOCS
    # set all SEEN_IN_DOC values to False for all words in the previous document
    print "updating EOD"
    for word in words_in_doc:
        vocab[word][SEEN_IN_DOC] = False
    # end padding
    write_to_file('data/test/1.txt', str(2))
    # end of document
    write_to_file('data/test/1.txt', str(1))
    # update frequencies
    vocab[BEG_PAD][FREQUENCY] += 1
    vocab[EOD][FREQUENCY] += 1
    vocab[END_PAD][FREQUENCY] += 1
    TOTAL_DOCS += 1

import spacy

nlp = spacy.load('en')
import sys

reload(sys)
sys.setdefaultencoding('utf8')

#os.path.join('data/split_corpus_files/','WestburyLab.Wikipedia.Corpus_1000000.txt')

import in_place

######################
### RUN EVERYTHING ###
######################

# write the beginning padding
write_to_file('data/test/1.txt', str(1))

with open('data/test/corpus/WestburyLab.Wikipedia.Corpus_1000000.txt', 'r') as corpus:
    words_in_doc = set()
    for line in corpus:

        if line.strip() == WIKI_EOD:
            update_eod(words_in_doc)
            continue
        sentence = nlp(unicode(line.strip()), "utf-8")

        for token in sentence:
            text = token.text
            pos = token.pos_
            word = text.lower() + '_' + pos.lower()
            if word not in vocab:
                word_id = set_up_word(text, pos, vocab)
            else:
                word_id = update_word(text, pos, vocab)
            if word_id != None:
                words_in_doc.add(word)
                write_to_file('data/test/1.txt', str(word_id))

########################
### WRITE VOCAB FILE ###
########################

for word in vocab:
    info = str(word) + " " + str(vocab[word][WORD_ID]) + " " + str(vocab[word][FREQUENCY])
    write_to_file('data/test/vocab.txt', info)

########################
### WRITE DF FILE ###
########################

global TOTAL_DOCS
write_to_file('data/test/df.txt', str(TOTAL_DOCS))

for word in vocab:
    write_to_file('data/test/df.txt', str(vocab[word][NUM_DOCS]))
