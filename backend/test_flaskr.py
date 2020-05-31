import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_ques = {
            'question': 'Who is the Chacha chaudry of world?',
            'answer': 'Do,land Trump',
            'category': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test categories that return '200'
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # Test questions with paging that return '200'
    def test_get_peginated_questions_with_categories(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['categories'])

    # Test paginate questions error '404' not found! .
    def test_404_get_peginate_questions_with_categories(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test delete questions with '200 ok' .
    def test_delete_question(self):
        question = Question(question="new question",
                            answer="new answer", difficulty=1, category=1)
        question.insert()
        ques_id = question.id
        res = self.client().delete(f'/questions/{ques_id}/delete')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == ques_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], ques_id)
        self.assertEqual(question, None)

    # Test delete if unprocessable error '422' .
    def test_422_if_questions_does_not_exist(self):
        res = self.client().delete('/questions/1000/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test delete if not found error '404' .
    def test_delete_question_404_not_found(self):
        res = self.client().delete("questions/anything/delete")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test delete if method not allowed error '405' .
    def test_delete_method_not_allowed_405(self):
        res = self.client().get("questions/1000/delete")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "method not allowed")

    # Test create new question
    def test_add_new_question(self):
        self.new_ques['difficulty'] = 1
        len_before = len(Question.query.all())
        res = self.client().post('/questions/add', json=self.new_ques)
        data = json.loads(res.data)
        len_after = len(Question.query.all())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertEqual(len_after, len_before + 1)

    # Test create new question 'unprocessable' error '422'
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions/add', json=self.new_ques)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test 405 error create new question method not allowed .
    def test_405_question_creation_method_not_allowed(self):
        res = self.client().get('/questions/add', json=self.new_ques)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test search question
    def test_get_question_search_with_results(self):
        res = self.client().post(
            '/questions/search', json={'searchTerm': 'you'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 2)
        self.assertEqual(data['current_category'], None)

    # Test '404' if error 'not found' search question .
    def test_404_error_no_search_results(self):
        res = self.client().post('/questions/search', json={'search': 'absd'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test '200' play quiz
    def test_play_quizzes(self):
        quiz_data = {"previous_questions": [],
                     "quiz_category": {"type": "", "id": 1}}
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # Test '405' if error 'method not allowed' play quiz
    def test_405_play_quizzes_method_not_allowed(self):
        quiz_data = {"previous_questions": [],
                     "quiz_category": {"type": "", "id": 1}}
        res = self.client().get('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test '422' if error 'unprocessable' play quiz
    def test_422_play_quizzes_unprocessable(self):
        quiz_data = {"previous_questions": []}
        res = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
