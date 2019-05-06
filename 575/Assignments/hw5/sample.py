from gensen import GenSen, GenSenSingle
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from matplotlib import pyplot

shakespeare = ['You speak an infinite deal of nothing.','These violent delights have violent ends And in their triump die, like fire and powder Which, as they kiss, consume']
trump = ['The Kentucky Derby decision was not a good one. It was a rough & tumble race on a wet and sloppy track, actually, a beautiful thing to watch. Only in these days of political correctness could such an overturn occur. The best horse did NOT win the Kentucky Derby - not even close!','I am pleased to inform all of those that believe in a strong, fair and sound Immigration Policy that Mark Morgan will be joining the Trump Administration as the head of our hard working men and women of ICE. Mark is a true believer and American Patriot. He will do a great job!']
obama = ['Condolences to the family of John Singleton. His seminal work, Boyz n the Hood, remains one of the most searing, loving portrayals of the challenges facing inner-city youth. He opened doors for filmmakers of color to tell powerful stories that have been too often ignored.','This generation of climate activists is tired of inaction, and theyve caught the attention of leaders all over the world. So while this challenge is only getting more urgent, they show us the kind of action itll take to meet this moment.']
idx2speaker = ['trump1','trump2','obama1','obama2','shakespeare1','shakespeare2']
sentences = trump + obama + shakespeare
gensen_1 = GenSenSingle(
    model_folder='./data/models',
    filename_prefix='nli_large_bothskip',
    pretrained_emb='./data/embedding/glove.840B.300d.h5'
)
reps_h, reps_h_t = gensen_1.get_representation(
    sentences, pool='last', return_numpy=True, tokenize=True
)
x = []
for i in range(len(reps_h)):
    x.append(reps_h[i].mean(axis=0))

model = TSNE(n_components=2, perplexity=30, init='pca', method='exact', n_iter=5000)
x = model.fit_transform(x)
pyplot.figure(figsize=(50,50))
for i in range(len(x)):
    pyplot.text(x[i, 0], x[i, 1], idx2speaker[i], bbox=dict(facecolor='blue', alpha=0.1))

pyplot.xlim((np.min(x[:, 0]), np.max(rxt[:, 0])))
pyplot.ylim((np.min(x[:, 1]), np.max(x[:, 1])))
pyplot.savefig('TSNEGlove.png')