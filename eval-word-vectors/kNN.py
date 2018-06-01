from scipy.spatial.distance import cosine
import numpy as np
import heapq
from ranking import cosine_sim

import sys

def cosineSim(senseVec1, senseVec2):  # TODO: compare this to Faruqui's cosine_sim
	return 1-abs(cosine(senseVec1,senseVec2))

def avgSim(senseVecs1, senseVecs2):
	similarities = []
	k1 = len(senseVecs1)
	k2 = len(senseVecs2)
	for i in xrange(k1):
		for j in xrange(k2):
			similarities.append(cosine_sim(senseVecs1[i],senseVecs2[j]))
	return np.sum(similarities)/(k1*k2)

def maxSim(senseVecs1, senseVecs2):
	maxSimilarity = float(-inf)
	k1 = len(senseVecs1)
	k2 = len(senseVecs2)
	for i in xrange(k1):
		for j in xrange(k2):
			pass

def kNN_perSense(word_senses_map, word, k):
	for senseIdx, sense in enumerate(word_senses_map[word]):
		print word, senseIdx
		q = []
		for neighbor in word_senses_map:
			if neighbor == word:
				continue
			for neighborIdx, neighborSense in enumerate(word_senses_map[neighbor]):
				cosSim = 1-abs(cosine(sense,neighborSense))
				if len(q) < k:
					heapq.heappush(q, (cosSim, neighbor+str(neighborIdx)))
				elif cosSim >= q[0][0]:
					heapq.heappop(q)
					heapq.heappush(q, (cosSim, neighbor+str(neighborIdx)))

		print sorted(q,reverse=True)

def kNN_avgSim(word_senses_map, word, k):
	q = []
	for neighbor in word_senses_map:
		if neighbor == word:
			continue
		avgCos = avgSim(word_senses_map[word], word_senses_map[neighbor])
		if len(q) < k:
			heapq.heappush(q, (avgCos, neighbor))
		elif avgCos >= q[0][0]:
			heapq.heappop(q)
			heapq.heappush(q, (avgCos, neighbor))
	print sorted(q, reverse=True)

def load_mssg_senses(file):
	word_senses_map = {}
	with open(file, 'rb') as f:
		line = f.readline().strip('n')
		tokens = line.split()
		vocab_size = int(tokens[0])
		dimension = int(tokens[1])
		print vocab_size, dimension

		for i in xrange(vocab_size):
			tokens = f.readline().strip('\n').split()
			word, num_senses = tokens[0], int(tokens[1])
			global_vector = f.readline().strip('\n')
			senses = []
			for j in xrange(num_senses):
				senseVec = f.readline().strip('\n')
				clusterCenter = f.readline().strip('\n')
				senses.append(np.array(map(float, senseVec.split())))
			word_senses_map[word] = senses
	return word_senses_map

def load_hsm_senses(vocab_file, wordreps_file):
	import scipy.io
	vocab_data = scipy.io.loadmat(vocab_file)
	vocab = vocab_data['vocab']
	tfidf_count = vocab_data['tfidf']
	num_prototypes = vocab_data['numEmbeddings']
	word_embeddings = scipy.io.loadmat(wordreps_file)['We']
	word_senses_map = {}
	for idx, word in enumerate(vocab[0]):
		num_senses = num_prototypes[0][idx]
		word_senses_map[word[0]] = word_embeddings[:,idx,:num_senses].transpose((1,0))
	return word_senses_map


def main(query_word):
	# word_senses_map = load_hsm_senses('data/vocab.mat', 'data/wordreps.mat')

	# word_senses_map = load_mssg_senses('data/vectors-MSSG-50D-6K.txt')
	word_senses_map = load_mssg_senses('data/vectors-NP-MSSG-50D-6K.txt')
	kNN_perSense(word_senses_map, query_word, 10)
	
if __name__ == '__main__':
	query_word = sys.argv[1]
	print query_word
	main(query_word)