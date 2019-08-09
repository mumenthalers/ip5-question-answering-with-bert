import pandas as pd
from matplotlib import pyplot


data = pd.read_csv('./out/evaluation.csv', sep=',', header=0, index_col="model")
data.columns = ['k_mean_accuracy', 'eval_set_accuracy']

steps = range(0, len(data))

fig = pyplot.figure()
ax = fig.add_subplot(111)
ax.set_ylim(0.75, 0.83)
ax.set_xlabel("Steps (×1000) (0 is pretrained Bert Base)")
ax.plot(steps, data['k_mean_accuracy'], '-', label='Accuracy of K-Mean Clusters')
ax.legend(loc='lower left')
ax2 = ax.twinx()
ax2.plot(steps, data['eval_set_accuracy'], '-r', label='Accuracy of Question to Topic Assignment')
ax2.set_ylim(0.87, 0.95)
ax2.legend(loc='upper right')
fig.savefig(fname='./out/evaluation.svg', format='svg')
pyplot.show()



def print_head_n_tail(df, n=3):
    head = df[:n]
    head.loc['----'] = ['-', '-']
    tail = df[-n:]
    head_tail = pd.concat([head, tail])
    print(head_tail)

print('\n\n\nBERT BASE VALUES')
print(data.loc['bert_model.ckpt'])


d1 = data.sort_values(by='eval_set_accuracy', ascending=False)
print('\n\n\n#sorted by accuracy of Question to Topic Assignment')
print_head_n_tail(d1)

d2 = data.sort_values(by='k_mean_accuracy', ascending=False)
print('\n\n\n#sorted by accuracy of K-Mean Clusters')
print_head_n_tail(d2)
