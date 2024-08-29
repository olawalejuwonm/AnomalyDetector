import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import os
from main import SurveillanceSystem

class TestSurveillanceSystem(unittest.TestCase):

    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "fake_token", "TELEGRAM_CHAT_ID": "fake_chat_id"})
    @patch('cv2.VideoCapture')
    def setUp(self, mock_video_capture):
        self.system = SurveillanceSystem()
        self.system.camera = MagicMock()
        self.system.camera.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))

    def test_initialization(self):
        self.assertIsNotNone(self.system.model)
        self.assertIsNotNone(self.system.tracker)
        self.assertIsNotNone(self.system.box_annotator)
        self.assertIsNotNone(self.system.label_annotator)
        self.assertIsNotNone(self.system.trace_annotator)
        self.assertEqual(self.system.bot_token, "fake_token")
        self.assertEqual(self.system.chat_id, "fake_chat_id")
        self.assertFalse(self.system.is_recording)
        self.assertEqual(self.system.record_duration, 20)
        self.assertEqual(self.system.video_directory, "static/recorded_videos")

    @patch('requests.post')
    def test_send_telegram_message(self, mock_post):
        mock_post.return_value.json.return_value = {"ok": True}
        response = self.system.send_telegram_message("Test message")
        self.assertEqual(response, {"ok": True})
        mock_post.assert_called_once_with(
            "https://api.telegram.org/botfake_token/sendMessage",
            data={"chat_id": "fake_chat_id", "text": "Test message"}
        )

    # @patch('builtins.open', new_callable=unittest.mock.mock_open)
    # @patch('json.dump')
    # def test_write_metadata_to_file(self, mock_json_dump, mock_open):
    #     self.system.metadata = {
    #         "file_name": "test_file",
    #         "start_time": "2023-01-01 00:00:00",
    #         "detections": {}
    #     }
    #     self.system.frame_count = 40
    #     self.system.write_metadata_to_file()
    #     expected_path = os.path.normpath(os.path.join('static', 'recorded_videos', 'test_file.json'))
    #     actual_path = os.path.normpath(mock_open.call_args[0][0])
    #     self.assertEqual(expected_path, actual_path)
    #     mock_open.assert_called_once_with(expected_path, 'w')
    #     mock_json_dump.assert_called_once()

    @patch('cv2.VideoWriter')
    def test_start_new_recording(self, mock_video_writer):
        self.system.start_new_recording()
        self.assertIsNotNone(self.system.out)
        self.assertIn("file_name", self.system.metadata)
        self.assertIn("detections", self.system.metadata)
        self.assertIn("start_time", self.system.metadata)

    @patch('threading.Thread')
    def test_process_frame(self, mock_thread):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        processed_frame = self.system.process_frame(frame)
        self.assertIsNotNone(processed_frame)
        if self.system.is_recording:
            self.assertTrue(mock_thread.called)

    @patch('cv2.imshow')
    @patch('cv2.waitKey', return_value=ord('q'))
    def test_run(self, mock_wait_key, mock_imshow):
        self.system.run()
        self.system.camera.read.assert_called()
        mock_imshow.assert_called()
        self.system.camera.release.assert_called()

if __name__ == '__main__':
    unittest.main()