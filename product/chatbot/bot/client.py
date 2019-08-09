from chatbot.errors import NoQuestionProvidedError
from bert_serving.client import BertClient
from chatbot import db
from scipy import spatial
import numpy as np
import os


class Client:

    bc = None
    tree = None
    questions = []

    @classmethod
    def close(self):
        if self.bc is not None:
            self.bc.close()

    @classmethod
    def _encode(self, question):
        if self.bc is not None:
            return self.bc.encode([question])

    @classmethod
    def warmup(self, app):
        with app.app_context():
            # Connect the client with the ber-server network when running in docker
            if 'DOCKER' in os.environ:
                self.bc = BertClient(ip='bert-server')
            else:
                self.bc = BertClient()
            self.questions = db.fetch_all_questions()
            question_texts = list(map(lambda q: q['text'], self.questions))
            question_vecs = self.bc.encode(question_texts)
            self.tree = spatial.KDTree(question_vecs)

    @classmethod
    def ask(self, question):
        if question is None:
            raise NoQuestionProvidedError
        question_vec = self._encode(question)
        _, indexes = self.tree.query(question_vec)
        return self.questions[indexes[0]]['topic']

    @classmethod
    def add_question(self, text, topic):
        db.insert_question(text, topic)
        np.append(self.tree.data, self._encode(text)[0])
