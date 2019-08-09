#!/bin/bash

GS_BUCKET_DIR="gs://colab-bert/engadget_L-12_H-768_A-12"

BASE_MODEL_DIR="~/Downloads/uncased_L-12_H-768_A-12"
TUNED_MODEL_DIR="./out/checkpoints"

echo "evaluate bert base model"
python evaluate.py -model_dir=$BASE_MODEL_DIR

for i in {1..200}; do
    CHECKPOINT_NUM=$(bc <<< "$i*1000")

    echo "download model for checkpoint model.ckpt-$CHECKPOINT_NUM"

    INDEX_NAME="model.ckpt-$CHECKPOINT_NUM.index"
    META_NAME="model.ckpt-$CHECKPOINT_NUM.meta"
    DATA_NAME="model.ckpt-$CHECKPOINT_NUM.data-00000-of-00001"

    TARGET_DIR="out/checkpoints"
    if ! test -f "$TARGET_DIR/$INDEX_NAME";then
        gsutil cp "$GS_BUCKET_DIR/$INDEX_NAME" "$TARGET_DIR/$INDEX_NAME"
    fi
    if ! test -f "$TARGET_DIR/$META_NAME";then
        gsutil cp "$GS_BUCKET_DIR/$META_NAME" "$TARGET_DIR/$META_NAME"
    fi
    if ! test -f "$TARGET_DIR/$DATA_NAME";then
     gsutil cp "$GS_BUCKET_DIR/$DATA_NAME" "$TARGET_DIR/$DATA_NAME"
    fi

    echo "evaluate model for checkpoint mode.ckpt-$CHECKPOINT_NUM"
    python evaluate.py -model_dir=$BASE_MODEL_DIR -tuned_model_dir=$TUNED_MODEL_DIR -ckpt_name="model.ckpt-$CHECKPOINT_NUM"

    # clear temp directories from optimized model from BaaS
    rm -rf /home/simon/dev/ip5-bert/tmp*

    rm "$TARGET_DIR/$INDEX_NAME"
    rm "$TARGET_DIR/$META_NAME"
    rm "$TARGET_DIR/$DATA_NAME"
done
