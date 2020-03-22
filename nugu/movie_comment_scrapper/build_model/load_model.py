from gensim.models.word2vec import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import matplotlib

font_name = matplotlib.font_manager.FontProperties(
                fname="C:/Windows/Fonts/gulim.ttc"  # 한글 폰트 위치를 넣어주세요
            ).get_name()
matplotlib.rc('font', family=font_name)

def plot_2d_graph(vocabs, xs, ys): 
    plt.figure(figsize=(8,6))
    plt.scatter(xs, ys, marker ='o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))
    plt.show()

model = Word2Vec.load('../20191124_0200')



word_vectors = model.wv

print(model.wv['김혜수'])
print(model.wv.most_similar('욕정'))
print(model.wv.most_similar('재미'))
print(model.wv.most_similar('재밌'))
print(model.most_similar(positive=['김혜수', '레이첼'], negative=['여자', '여배우'],  topn=10))
vocabs = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

# pca = PCA(n_components=2)
# xys = pca.fit_transform(word_vectors_list)
# xs = xys[:, 0]
# ys = xys[:, 1]
#
#plot_2d_graph(vocabs, xs, ys)





# from sklearn.decomposition import IncrementalPCA    # inital reduction
# from sklearn.manifold import TSNE                   # final reduction
# import numpy as np                                  # array handling
# from gensim.models.word2vec import Word2Vec
# import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
# import matplotlib
# from plotly.offline import init_notebook_mode, iplot, plot
# import plotly.graph_objs as go
# import random
#
# font_name = matplotlib.font_manager.FontProperties(
#                 fname="C:/Windows/Fonts/gulim.ttc"  # 한글 폰트 위치를 넣어주세요
#             ).get_name()
# matplotlib.rc('font', family=font_name)
# model = Word2Vec.load('20191123_2300')
#
# def reduce_dimensions(model):
#     num_dimensions = 2  # final num dimensions (2D, 3D, etc)
#
#     vectors = [] # positions in vector space
#     labels = [] # keep track of words to label our data again later
#     for word in model.wv.vocab:
#         vectors.append(model.wv[word])
#         labels.append(word)
#
#     # convert both lists into numpy vectors for reduction
#     vectors = np.asarray(vectors)
#     labels = np.asarray(labels)
#
#     # reduce using t-SNE
#     vectors = np.asarray(vectors)
#     tsne = TSNE(n_components=num_dimensions, random_state=0)
#     vectors = tsne.fit_transform(vectors)
#
#     x_vals = [v[0] for v in vectors]
#     y_vals = [v[1] for v in vectors]
#     return x_vals, y_vals, labels
#
#
# x_vals, y_vals, labels = reduce_dimensions(model)
#
# def plot_with_plotly(x_vals, y_vals, labels, plot_in_notebook=True):
#
#     trace = go.Scatter(x=x_vals, y=y_vals, mode='text', text=labels)
#     data = [trace]
#
#     if plot_in_notebook:
#         init_notebook_mode(connected=True)
#         iplot(data, filename='word-embedding-plot')
#     else:
#         plot(data, filename='word-embedding-plot.html')
#
#
# def plot_with_matplotlib(x_vals, y_vals, labels):
#
#     random.seed(0)
#
#     plt.figure(figsize=(12, 12))
#     plt.scatter(x_vals, y_vals)
#
#     #
#     # Label randomly subsampled 25 data points
#     #
#     indices = list(range(len(labels)))
#     selected_indices = random.sample(indices, 25)
#     for i in selected_indices:
#         plt.annotate(labels[i], (x_vals[i], y_vals[i]))
#     plt.show()
#
# try:
#     get_ipython()
# except Exception:
#     plot_function = plot_with_matplotlib
# else:
#     plot_function = plot_with_plotly
#
# plot_function(x_vals, y_vals, labels)