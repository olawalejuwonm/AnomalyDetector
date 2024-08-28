import unittest
import os
from unittest.mock import patch, MagicMock, mock_open
from flask import Flask
from app import app, get_video_files, video_gallery, check_videos, delete_video, run_main, start_flask

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # @patch('os.path.exists')
    # @patch('os.makedirs')
    # @patch('os.listdir')
    # def test_get_video_files(self, mock_listdir, mock_makedirs, mock_exists):
    #     mock_exists.side_effect = lambda x: x.endswith('recorded_videos')
    #     mock_listdir.return_value = ['video1.webm', 'video2.webm']
        
    #     video_directory, video_files = get_video_files()
        
    #     self.assertEqual(video_directory, os.path.join(app.static_folder, 'recorded_videos'))
    #     self.assertEqual(video_files, ['video1.webm', 'video2.webm'])
    #     mock_makedirs.assert_not_called()

    # @patch('app.get_video_files')
    # @patch('os.path.exists')
    # @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    # def test_video_gallery(self, mock_open, mock_exists, mock_get_video_files):
    #     mock_get_video_files.return_value = (os.path.join(app.static_folder, 'recorded_videos'), ['video1.webm'])
    #     mock_exists.return_value = True
        
    #     response = self.app.get('/')
        
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'video1.webm', response.data)
    #     self.assertIn(b'key', response.data)

    @patch('app.get_video_files')
    def test_check_videos(self, mock_get_video_files):
        mock_get_video_files.return_value = (os.path.join(app.static_folder, 'recorded_videos'), ['video1.webm'])
        
        response = self.app.get('/check-videos')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['video1.webm'])

    @patch('os.path.exists')
    @patch('os.remove')
    def test_delete_video(self, mock_remove, mock_exists):
        mock_exists.side_effect = lambda x: x.endswith('video1.webm') or x.endswith('video1.webm.json')
        
        response = self.app.post('/delete-video', json={'file_name': 'video1.webm'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'success': 'video1.webm deleted successfully'})
        mock_remove.assert_called()

    @patch('subprocess.run')
    def test_run_main(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Script output', stderr='')
        
        response = self.app.post('/run-main')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'output': 'Script output'})

    @patch('waitress.serve')
    @patch('app.app.run')
    def test_start_flask(self, mock_run, mock_serve):
        start_flask(app=app, port=5000, host='0.0.0.0')
        
        mock_serve.assert_called_once_with(app, port=5000, host='0.0.0.0')
        mock_run.assert_not_called()

if __name__ == '__main__':
    unittest.main()