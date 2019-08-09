# Question Answer Bot

The Question Answer Bot is a HTTP REST Service inside a docker container for classifying sentences.

# Usage

First you have to have installed docker and docker-compose.

Build the docker file which is not on docker hub:

``` bash
docker build -t question-answer-bot
```

Start the docker container using docker-compose:

``` bash
docker-compose up
```

This command starts the bert-as-a-service server and the flask application to
receive questions to classify.

As soon as the bert-as-a-service server is started, the flask app will warm up
the questions. This means that all questions in the database are encoded and
loaded in a spatial KDTree.

More questions can be added on runtime.

# API

The whole api is reachable under the port `8000` when started in the docker container.

## Receive all reference questions

```http
GET /questions HTTP/1.1
Accept: application/json
```

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "text": "What about data protection with public cloud providers",
    "topic": "Cloud Services"
  }
]
```

## Add a new question on runtime

This will add the question to the KDTree as well as to the database for later warmup.

``` http
POST /questions HTTP/1.1
Accept: application/json
Content-Type: application/json

{
  "text": "What are the dangers of digitization?",
  "topic": "Digitalisierung"
}
```

```http
HTTP/1.1 204 No Content
```

## Ask for question

Accepts the question as a query parameter to be classified and returns the topic.

```http
GET /bot?question=Wie%20viele%20Mitarbeiter%20seid%20ihr HTTP/1.1
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "topic": "Digitalisierung"
}
```

# Development

For development, just the bert-as-a-service container needs to be started:

``` bash
docker run -it -p 5555:5555 -p 5556:5556 -p 9000:9000 bert-as-a-service
```

Now the flask dev server can be started:

``` bash
export FLASK_APP=chatbot
export FLASK_ENV=development

flask run
```

By default the flask app binds to port `5000`. Use `-p` to change that.

``` bash
flask run -p 8000
```
