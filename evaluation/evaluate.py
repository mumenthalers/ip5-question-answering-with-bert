import argparse
import csv
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from bert_serving.server.helper import get_args_parser, get_shutdown_parser
from bert_serving.server import BertServer
from bert_serving.client import BertClient
import time
time_started = time.time()

BERT_SERVER_PORT = 5555


parser = argparse.ArgumentParser(description='Evaluate BERT Model')
parser.add_argument('-model_dir', type=str, required=True, help='directory of a pretrained BERT model')
parser.add_argument('-tuned_model_dir', type=str, help='directory of a fine-tuned BERT model')
parser.add_argument('-ckpt_name', type=str, default='bert_model.ckpt', help='filename of the checkpoint file.')
eval_args = parser.parse_args()

print(f'EVALUATE MODEL {eval_args.ckpt_name}')


def read_questions(bc, data_set_name):
    with open(f'./out/{data_set_name}.csv') as f:
        data = list(csv.reader(f))
        topics = [topic_question[0] for topic_question in data]
        vectors = bc.encode([topic_question[1] for topic_question in data])
    return topics, np.array(vectors)


#  startup bert-as-a-service server and return ready to use BertClient
def start_baas():
    str_args = [
        '-model_dir', eval_args.model_dir,
        '-num_worker', '1',
        '-max_seq_len', 'NONE',
        '-port', f'{BERT_SERVER_PORT}'
    ]
    if eval_args.tuned_model_dir is not None:
        str_args = str_args + [
            '-tuned_model_dir', eval_args.tuned_model_dir,
            '-ckpt_name', eval_args.ckpt_name,
        ]
    print('server::construct')
    server = BertServer(get_args_parser().parse_args(str_args))
    print('server::start')
    server.start()
    print('server::wait')
    server.is_ready.wait()
    print('server::is_ready')

    return BertClient(port=BERT_SERVER_PORT)


# close given BertClient and shutdown bert-as-a-service
def stop_baas(bc):
    bc.close()
    args = get_shutdown_parser().parse_args([
        '-port', f'{BERT_SERVER_PORT}'
    ])
    BertServer.shutdown(args)


# cluster all sentences with k-mean (k=amount of topics) and return accuracy of the clusters
def evaluate_accuracy_with_k_mean_clustering(all_topics, vectors):
    topics = set(all_topics)
    topic_count = len(topics)
    kmeans = KMeans(n_clusters=topic_count)
    kmeans.fit(vectors)
    features = pd.DataFrame()
    features['topic'] = all_topics
    features['cluster'] = kmeans.labels_
    groups = features.groupby("cluster")

    # count sentences by topic per cluster
    count_by_cluster = {}
    for k, count in groups['topic'].value_counts().iteritems():
        cluster, topic = k
        if cluster not in count_by_cluster:
            count_by_cluster[cluster] = {}

        count_by_cluster[cluster][topic] = count

    correctly_assigned_sentences_in_cluster = 0

    # assign the clusters to a topic.
    topics_to_assign = list(topics)
    cluster_topic_assignment = {}
    for i in range(0, topic_count):
        next_count_to_assign = 0
        # it can happen, that there's a remaining topic,
        # but none of the clustered sentences in the remaining clusters contain a sentence of this very topic.
        # bad. but can happen. so we already assign the first topic of the remaining topics_to_assign
        temp_cluster_index = next(iter(count_by_cluster))
        temp_topic = topics_to_assign[0]
        for cluster_index, clusterdata in count_by_cluster.items():
            biggest_count_inside_cluster = 0
            temp_inner_topic = None
            for topic in topics_to_assign:
                if clusterdata.get(topic, 0) > biggest_count_inside_cluster:
                    biggest_count_inside_cluster = clusterdata[topic]
                    temp_inner_topic = topic

            if biggest_count_inside_cluster > next_count_to_assign:
                next_count_to_assign = biggest_count_inside_cluster
                temp_cluster_index = cluster_index
                temp_topic = temp_inner_topic

        correctly_assigned_sentences_in_cluster += next_count_to_assign
        cluster_topic_assignment[temp_topic] = [count_by_cluster.pop(temp_cluster_index)]
        topics_to_assign.remove(temp_topic)

    return correctly_assigned_sentences_in_cluster / len(vectors)


# find nearest neighbour for each eval question inside the reference questions.
# return accuracy of correctly assigned evaluation questions
def evaluate_accuracy_with_eval_questions(ref_top, ref_vecs, eval_top, eval_vecs):

    evalset_actual_topics = []
    evalset_pred_topics = []

    for ix, vec in enumerate(eval_vecs):
        score = np.sum(vec * ref_vecs, axis=1) / np.linalg.norm(ref_vecs, axis=1)
        pred_idx = np.argsort(score)[::-1][:1][0]
        evalset_pred_topics = evalset_pred_topics + [ref_top[pred_idx]]
        evalset_actual_topics = evalset_actual_topics + [eval_top[ix]]

    # import nltk
    # print(nltk.ConfusionMatrix(evalset_actual_topics, evalset_pred_topics))

    t = len(evalset_actual_topics)
    c = 0
    for idx, val in enumerate(evalset_actual_topics):
        if evalset_pred_topics[idx] == val:
            c += 1

    return c / t


# start BaaS an encode all reference and evaluation questions
bc = start_baas()
ref_topics, ref_vectors = read_questions(bc, 'training')
eval_topics, eval_vectors = read_questions(bc, 'testing')
stop_baas(bc)

# how accurate can unknown question be assigned to the reference questions?
accuracy_question_assignment = evaluate_accuracy_with_eval_questions(ref_topics, ref_vectors, eval_topics, eval_vectors)
print(f'accuracy with evaluation question set: {accuracy_question_assignment}')

# how accurate can unknown questions be correctly clustered?
k_mean_accuracy_values = []
for i in range(0, 10):
    k_mean_accuracy_values.append(evaluate_accuracy_with_k_mean_clustering(eval_topics, eval_vectors))
accuracy_k_mean_clustering = np.mean(k_mean_accuracy_values)
print(f"accuracy of k_mean clustering: {accuracy_k_mean_clustering}")

if not os.path.isfile('out/evaluation.csv'):
    with open('out/evaluation.csv', 'w+') as f:
        f.write('model,k_mean_accuracy,eval_set_accuracy\n')

with open('out/evaluation.csv', 'a') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow([
        eval_args.ckpt_name,
        accuracy_k_mean_clustering,
        accuracy_question_assignment
    ])

print(f"evaluation duration: {time.time() - time_started}s")