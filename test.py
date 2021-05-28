from unittest import TestCase
from app import app
from flask import checkion
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Setup Test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_page(self):
        """Test page"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', checkion)
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)


    def test_invalid_word(self):
        """Test for invalid word"""

        self.client.get('/')
        response = self.client.get('/check-word?word=Batman')
        self.assertEqual(response.json['result'], 'not-on-board')


    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=00000000000000000000000000000')
        self.assertEqual(response.json['result'], 'not-word')


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the checkion"""

        with self.client as client:
            with client.checkion_transaction() as check:
                check['board'] = [["B", "I", "N", "G", "O"], 
                                 ["I", "I", "N", "G", "P"], 
                                 ["N", "I", "N", "G", "E"], 
                                 ["G", "I", "N", "G", "N"], 
                                 ["O", "I", "N", "G", "S"]]
        response = self.client.get('/check-word?word=Bingo')
        self.assertEqual(response.json['result'], 'ok')


