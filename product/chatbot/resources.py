from flask_restful import Resource, reqparse, abort
from chatbot import db
from chatbot.bot.client import Client
from chatbot.errors import APIException


parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help='Text of the question')
parser.add_argument('topic', type=str, help='Topic of the question')
parser.add_argument(
    'question',
    type=str,
    help='Question to get topic for',
)


class Question(Resource):

    def get(self):
        return db.fetch_all_questions()

    def post(self):
        args = parser.parse_args()
        text = args['text']
        topic = args['topic']
        Client.add_question(text, topic)
        return '', 204


class Bot(Resource):

    def get(self):
        args = parser.parse_args()
        question = args['question']
        try:
            topic = Client.ask(question)
        except APIException as e:
            abort(e.code, message=str(e))
        return {
            'topic': topic,
        }
