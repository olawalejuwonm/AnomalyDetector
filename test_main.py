import unittest
from unittest.mock import patch, MagicMock
import numpy as np
import os
from main import SurveillanceSystem
import json


class TestSurveillanceSystem(unittest.TestCase):

    @patch.dict(
        os.environ,
        {"TELEGRAM_BOT_TOKEN": "fake_token", "TELEGRAM_CHAT_ID": "fake_chat_id"},
    )
    @patch("cv2.VideoCapture")
    def setUp(self, mock_video_capture):
        self.system = SurveillanceSystem()
        self.system.camera = MagicMock()
        self.system.camera.read.return_value = (
            True,
            np.zeros((480, 640, 3), dtype=np.uint8),
        )

    @patch("http.client.HTTPSConnection")
    def test_send_telegram_message(self, mock_https_connection):
        mock_conn = MagicMock()
        mock_https_connection.return_value = mock_conn
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({"ok": True}).encode("utf-8")
        mock_conn.getresponse.return_value = mock_response

        response = self.system.send_telegram_message("Test message")
        self.assertTrue(response["ok"])
        mock_https_connection.assert_called_once_with("api.telegram.org")
        mock_conn.request.assert_called_once_with(
            "POST",
            f"https://api.telegram.org/bot{self.system.bot_token}/sendMessage",
            body=json.dumps({"chat_id": self.system.chat_id, "text": "Test message"}),
            headers={"Content-Type": "application/json"},
        )

    @patch("http.client.HTTPSConnection")
    def test_send_telegram_frame(self, mock_https_connection):
        mock_conn = MagicMock()
        mock_https_connection.return_value = mock_conn
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({"ok": True}).encode("utf-8")
        mock_conn.getresponse.return_value = mock_response

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        response = self.system.send_telegram_frame(frame, "test_frame.jpg")
        self.assertTrue(response["ok"])
        mock_https_connection.assert_called_once_with("api.telegram.org")
        mock_conn.request.assert_called_once()

    @patch.object(SurveillanceSystem, "send_telegram_message")
    @patch.object(SurveillanceSystem, "send_telegram_frame")
    @patch("concurrent.futures.ThreadPoolExecutor")
    def test_run_telegram_tasks_in_thread(
        self, mock_executor, mock_send_frame, mock_send_message
    ):
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance

        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.system.run_telegram_tasks_in_thread("Test message", frame)

        mock_executor_instance.submit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
