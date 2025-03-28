import unittest
import shutil
import os
from app import app

class CMSTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_path, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)

    def create_document(self, name, content=""):
        with open(os.path.join(self.data_path, name), 'w') as file:
            file.write(content)

    def test_index(self):
        self.create_document('about.md')
        self.create_document("changes.txt")

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn("about.md", response.get_data(as_text=True))
        self.assertIn("changes.txt", response.get_data(as_text=True))

    def test_viewing_text_document(self):
        self.create_document("history.txt",
                             "Python 0.9.0 (initial release) is released.")
        
        with self.client.get('/history.txt') as response:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "text/plain; charset=utf-8")
            self.assertIn("Python 0.9.0 (initial release) is released.",
                        response.get_data(as_text=True))
            
    def test_viewing_nonexistant_document(self):
        with self.client.get("/notafile.ext") as response:
            self.assertEqual(response.status_code, 302)

        # Verify redirect and message handling works
        with self.client.get(response.headers['Location']) as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("notafile.ext does not exist",
                          response.get_data(as_text=True))

        # Assert that a page reload removes the message
        with self.client.get("/") as response:
            self.assertNotIn("notafile.ext does not exist",
                             response.get_data(as_text=True))
            
    def test_viewing_markdown_document(self):
        self.create_document("about.md", "# Python is...")

        response = self.client.get('/about.md')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
        self.assertIn("<h1>Python is...</h1>", response.get_data(as_text=True))
    
    def test_editing_document(self):
        self.create_document("changes.txt")

        response = self.client.get("/changes.txt/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn("<textarea", response.get_data(as_text=True))
        self.assertIn('<button type="submit"', response.get_data(as_text=True))

    def test_updating_document(self):
        response = self.client.post("/changes.txt/save",
                                    data={'content': "new content"})
        self.assertEqual(response.status_code, 302)

        follow_response = self.client.get(response.headers['Location'])
        self.assertIn("changes.txt has been updated",
                      follow_response.get_data(as_text=True))

        with self.client.get("/changes.txt") as content_response:
            self.assertEqual(content_response.status_code, 200)
            self.assertIn("new content",
                          content_response.get_data(as_text=True))
    
    def test_view_new_document_form(self):
        response = self.client.get('/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn("<input", response.get_data(as_text=True))
        self.assertIn('<button type="submit"', response.get_data(as_text=True))

    def test_create_new_document(self):
        response = self.client.post('/new',
                                    data={'file_name': 'test.txt'},
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.txt has been created",
                      response.get_data(as_text=True))

        response = self.client.get('/')
        self.assertIn("test.txt", response.get_data(as_text=True))

    def test_create_new_document_without_filename(self):
        response = self.client.post('/new', data={'file_name': ''})
        self.assertEqual(response.status_code, 422)
        self.assertIn("A name is required", response.get_data(as_text=True))

    def test_deleting_document(self):
        self.create_document("test.txt")

        response = self.client.post('/test.txt/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("test.txt has been deleted",
                      response.get_data(as_text=True))

        response = self.client.get('/')
        self.assertNotIn("test.txt", response.get_data(as_text=True))
        
if __name__ == '__main__':
    unittest.main()