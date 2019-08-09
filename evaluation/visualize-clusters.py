from bert_serving.client import BertClient
import csv
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold
import numpy as np


# make sure bert-as-a-service is running:
# bert-serving-start -model_dir ~/Downloads/uncased_L-12_H-768_A-12 -num_worker=1


with open('./data/sample.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = [[qna[0], qna[1]] for qna in csv_reader]
    topics = list(set([qna[0] for qna in data]))
    print(f"{len(topics)} topics, {len(data)} questions")

markers = ["o", "x", '^', "s", "d", "1", "|", "_", "+", "*", 11, "P", ".", "p", "D"]
colors = [
    "#2980B9",
    "#9B59B6",
    "#E74C3C",
    "#DAF7A6",
    "#FFC300",
    "#C0CA33",
    "#43A047",
    "#00ACC1",
    "#1E88E5",
    "#5E35B1",
    "#D81B60",
    "#827717",
    "#1B5E20",
    "#006064",
    "#0D47A1"
]

bc = BertClient()
all_vecs = []
questions_per_topic_count = []
vec_to_cluster = []
for ix, i in enumerate(topics):
    questions_for_topic = [qna[1] for qna in data if qna[0] == i]
    cluster_vecs = bc.encode(questions_for_topic)
    all_vecs.extend(cluster_vecs)

    for j in questions_for_topic:
        vec_to_cluster.append(ix)

    questions_per_topic_count.append(len(cluster_vecs))
    print(f"Topic {i}: {len(cluster_vecs)} questions")
bc.close()

# store as tsv
with open('./out/labels.tsv', 'w') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    tsv_writer.writerow(['topic', 'question'])
    for row in data:
        tsv_writer.writerow(row)
with open('./out/vectors.tsv', 'w') as f:
    tsv_writer = csv.writer(f, delimiter='\t')
    for row in all_vecs:
        tsv_writer.writerow(row)

# embed_pca_50d = decomposition.PCA(n_components=50).fit_transform(all_vecs)

# embed_pca_2d = decomposition.PCA(n_components=2).fit_transform(all_vecs)
embed_tsne_2d = manifold.TSNE(n_components=2).fit_transform(all_vecs)

# embed_pca_3d = decomposition.PCA(n_components=3).fit_transform(all_vecs)
embed_tsne_3d = manifold.TSNE(n_components=3).fit_transform(all_vecs)

embed2d = np.array(embed_tsne_2d)
embed3d = np.array(embed_tsne_3d)

# with open('./out/pca-tsne-2d.tsv', 'w') as f:
#     tsv_writer = csv.writer(f, delimiter='\t')
#     for row in embed_tsne_2d:
#         tsv_writer.writerow(row)

#
# with open('./out/pca-tsne-3d.tsv', 'w') as f:
#     tsv_writer = csv.writer(f, delimiter='\t')
#     for row in embed_tsne_3d:
#         tsv_writer.writerow(row)

c = 0
plots2d = []
plots3d = []

fig2d = pyplot.subplot()

# fig3d = pyplot.figure()
# ax3d = Axes3D(fig3d)

for ix, i in enumerate(topics):
    l = questions_per_topic_count[ix]
    X2d = embed2d[c:c + l]
    X3d = embed3d[c:c + l]
    c += l

    plots2d.append(
        fig2d.scatter(X2d[:, 0], X2d[:, 1], marker=markers[ix], color=colors[ix])
    )
    # plots3d.append(
    #     ax3d.scatter(X3d[:, 0], X3d[:, 1], X3d[:, 2], marker=markers[ix], color=colors[ix])
    # )

fig2d.legend(plots2d, topics,
             scatterpoints=1,
             loc='lower left',
             ncol=3,
             fontsize=8)
pyplot.savefig(fname='./out/visualize-clusters.svg', format='svg')

# fig3d.legend(plots3d, topics,
#              scatterpoints=1,
#              loc='lower left',
#              ncol=3,
#              fontsize=8)
pyplot.show()