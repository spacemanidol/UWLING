from gensen import GenSen, GenSenSingle
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from matplotlib import pyplot

shakespeare = ['You speak an infinite deal of nothing.','These violent delights have violent ends And in their triump die, like fire and powder Which, as they kiss, consume']
wutang = ['Raw Ima give it to ya, with no trivia Raw like cocaine straight from Bolivia','Yo, nobody budge while I shot slugs Never shot thugs, Im runnin with thugs that flood mugs']
lukecombs = ['Seventeen, you dont think that much about life You just live it Like Kerosene dancing around a fire But youre in','I picked myself up off the floor And found something new worth living for In an old dusty hand-me-down six string And a couple chords']
trump = ['The Kentucky Derby decision was not a good one. It was a rough & tumble race on a wet and sloppy track, actually, a beautiful thing to watch. Only in these days of political correctness could such an overturn occur. The best horse did NOT win the Kentucky Derby - not even close!','I am pleased to inform all of those that believe in a strong, fair and sound Immigration Policy that Mark Morgan will be joining the Trump Administration as the head of our hard working men and women of ICE. Mark is a true believer and American Patriot. He will do a great job!','For too long, a small group in our nations Capital has reaped the rewards of government while the people have borne the cost. Washington flourished -- but the people did not share in its wealth. Politicians prospered -- but the jobs left, and the factories closed.']
obama = ['Condolences to the family of John Singleton. His seminal work, Boyz n the Hood, remains one of the most searing, loving portrayals of the challenges facing inner-city youth. He opened doors for filmmakers of color to tell powerful stories that have been too often ignored.','This generation of climate activists is tired of inaction, and theyve caught the attention of leaders all over the world. So while this challenge is only getting more urgent, they show us the kind of action itll take to meet this moment.','That we are in the midst of crisis is now well understood. Our nation is at war, against a far-reaching network of violence and hatred. Our economy is badly weakened, a consequence of greed and irresponsibility on the part of some, but also our collective failure to make hard choices and prepare the nation for a new age. Homes have been lost; jobs shed; businesses shuttered. Our health care is too costly; our schools fail too many; and each day brings further evidence that the ways we use energy strengthen our adversaries and threaten our planet.']
idx2speaker = ['trump1','trump2','trumpinaguration','obama1','obama2','obamainaguration','shakespeare1','shakespeare2','wutang1','wutang2','lukecombs','lukecombs']
sentences = trump + obama + shakespeare + lukecombs + wutang
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

model = TSNE(n_components=2, perplexity=20, init='pca', method='exact', n_iter=5000)
x = model.fit_transform(x)
pyplot.figure(figsize=(20,20))
pyplot.xlim((np.min(x[:, 0])-10, np.max(x[:, 0])+10))
pyplot.ylim((np.min(x[:, 1])-10, np.max(x[:, 1])+10))
for i in range(len(x)):
    pyplot.text(x[i, 0], x[i, 1], idx2speaker[i], bbox=dict(facecolor='blue', alpha=0.1))

pyplot.savefig('TSNEGlove.png')
