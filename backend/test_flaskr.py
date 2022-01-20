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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_404_get_questions(self):
        response = self.client().get('/questions?page=5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        response = self.client().delete('/questions/4')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 4)

    def test_404_delete_question(self):
        response = self.client().delete('/questions/3210')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'])

    def test_add_question(self):
        question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }
        response = self.client().post('/questions', json=question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_405_question_addition_not_allowed(self):
        question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 2,
            'category': 2
        }
        response = self.client().post('/questions/45', json=question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'method not allowed')

    def test_search(self):
        response = self.client().post('/questions', json={'searchTerm': 'invented'})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_search_without_results(self):
        response = self.client().post('/questions', json={'searchTerm':'jkjnkjv'})

        data = json.loads(response.data)

        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(data['success'])

    def test_404_search_question(self):
        res = self.client().post('/questions/search', json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "resource not found")
    
    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['current_category'], 'Science')
        self.assertTrue(data['success'])

    def test_404_get_questions_by_category(self):
        response = self.client().get('/categories/1234/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])

    def test_play_quiz(self):
        quiz_round = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Geography',
                'id': 14
                }
            }
        response = self.client().post('/play', json=quiz_round)
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_422_play_quiz(self):
        quiz_round = {
            'previous_questions': []
        }
        response = self.client().post('/play', json=quiz_round)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()