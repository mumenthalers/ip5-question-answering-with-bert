FROM python:3

# Install python2.7 which is required for google-cloud-sdk
RUN apt-get update
RUN apt-get install python2.7

# Install google cloud skd
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz
# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh --quiet
# Add google-cloud-sdk to path
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Make dirs for models
RUN mkdir -p /app/base-models
RUN mkdir -p /app/trained-models/engadget_L-12_H-768_A-12

# Download base model
RUN gsutil cp -r gs://cloud-tpu-checkpoints/bert/uncased_L-12_H-768_A-12/ /app/base-models

# Download optimized models
RUN gsutil cp gs://colab-bert/engadget_L-12_H-768_A-12/model.ckpt-43000.data-00000-of-00001 /app/trained-models/engadget_L-12_H-768_A-12
RUN gsutil cp gs://colab-bert/engadget_L-12_H-768_A-12/model.ckpt-43000.index /app/trained-models/engadget_L-12_H-768_A-12
RUN gsutil cp gs://colab-bert/engadget_L-12_H-768_A-12/model.ckpt-43000.meta /app/trained-models/engadget_L-12_H-768_A-12

# Install bert server
RUN pip install -U bert-serving-server
RUN pip install -U tensorflow

# Install dependencies to start http health check http-server
RUN pip install -U bert-serving-client
RUN pip install -U flask
RUN pip install -U flask_compress
RUN pip install -U flask_cors
RUN pip install -U flask_json

# Setup working dir
WORKDIR /app
ADD entrypoint.sh /app/

# Define entrypoint which starts the bert server
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
