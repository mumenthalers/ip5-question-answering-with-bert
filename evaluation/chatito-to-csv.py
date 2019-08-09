import os
import json
import csv

# generate dataset first, or use datasets from './data/'
# data_dir = './data'
data_dir = '../chatito-questions/dist'


def convert(id):
    file_name = f'{data_dir}/default_dataset_{id}.json'

    if not os.path.isfile(file_name):
        raise FileNotFoundError(f'the file {file_name} does not exist. '
                                'Did you run the chatito question set generation? '
                                'You can also use the files provided in ./data/')

    with open(file_name) as fr:
        training = json.load(fr)

    if not os.path.exists('./out'):
        os.makedirs('./out')
    with open(f'./out/{id}.csv', 'w') as fw:
        csv_writer = csv.writer(fw)

        for key, value in training.items():
            for item in value:
                csv_writer.writerow([key, item[0]['value']])


convert('training')
convert('testing')
