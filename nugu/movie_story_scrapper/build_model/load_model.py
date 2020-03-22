from gensim.models.word2vec import Word2Vec

model = Word2Vec.load('story_20191205_1654')

word_vectors = model.wv

print(model.wv['스타워즈'])
print(model.wv.most_similar('욕정'))
print(model.wv.most_similar('재미'))
print(model.wv.most_similar('재밌'))
print(model.most_similar(positive=['김혜수', '레이첼'], negative=['여자', '여배우'],  topn=10))
vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]