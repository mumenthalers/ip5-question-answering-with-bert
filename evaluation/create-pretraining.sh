#!/usr/bin/env bash

BERT_BASE_DIR=~/Downloads/uncased_L-12_H-768_A-12
BERT_MAX_SEQ_LEN=128
BERT_MAX_PREDICTIONS_PER_SEQ=20

{ #try
python ./bert/create_pretraining_data.py \
  --input_file=./out/engadget-corpus.txt \
  --output_file=./out/engadget_tf_examples.tfrecord \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --do_lower_case=True \
  --max_seq_length=$BERT_MAX_SEQ_LEN \
  --max_predictions_per_seq=$BERT_MAX_PREDICTIONS_PER_SEQ \
  --masked_lm_prob=0.15 \
  --random_seed=12345 \
  --dupe_factor=5 &&

  echo "DONE. upload the file to google cloud storage for the training on colab"
} || { # catch
    echo "make sure the pretrained bert model exists at location $BERT_BASE_DIR"
}
