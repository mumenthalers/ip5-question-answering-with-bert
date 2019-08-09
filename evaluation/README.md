# evaluation
Scripts for prepare the training and run the evaluation

## Prerequisites
Make sure you have [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv)
installed.


## Script Description
| Script | Description |
| --- | ---|
| chatito-to-csv.py                | transform the json file generated by chatito to a simple csv|
| prepare-engadget-sentences.py    | transform the json file from _engadget-scrapper_ to a simple txt file|
| create-pretraining.sh            | transform the engadget-corputs.tx file to *.tfrecord with _create\_pretraining\_data.py_ from BERT|
| evaluate.py                      | run the actual evaluations on a given model|
| download-models-and-evaluate.sh* | bash script do download trained bert models from google cloud storage and run `evaluate.py` wihth it|
| visualize-clusters.py            | script to create a matplotlib chart from a the sample.csv (used for illustrative purpose)|
| visualize-evaluation.py          | script to create a matplotlib chart from the evaluation.csv (used for illustrative purpose)|

\* having [gsutils](https://cloud.google.com/storage/docs/gsutil) installed is necessary to run this script.