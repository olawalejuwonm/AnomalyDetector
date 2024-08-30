import unittest  # Import the unittest module for creating and running tests.
from unittest.mock import patch, MagicMock  # Import patch and MagicMock for mocking dependencies.
import numpy as np  # Import numpy for numerical operations, particularly for creating arrays.
import os  # Import the os module for interacting with the operating system.
from main import SurveillanceSystem  # Import the SurveillanceSystem class from the main module.
import json  # Import the json module for handling JSON data.

class TestSurveillanceSystem(unittest.TestCase):  # Define a test case class inheriting from unittest.TestCase.

    @patch.dict(  # Patch the os.environ dictionary to provide fake environment variables.
        os.environ,
        {"TELEGRAM_BOT_TOKEN": "fake_token", "TELEGRAM_CHAT_ID": "fake_chat_id"},
    )
    @patch("cv2.VideoCapture")  # Patch the cv2.VideoCapture class to mock the camera.
    def setUp(self, mock_video_capture):  # Define the setup method to initialize the test environment.
        self.system = SurveillanceSystem()  # Create an instance of the SurveillanceSystem class.
        self.system.camera = MagicMock()  # Mock the camera object.
        self.system.camera.read.return_value = (  # Set the return value of the camera's read method.
            True,
            np.zeros((480, 640, 3), dtype=np.uint8),  # Return a dummy frame.
        )

    @patch("http.client.HTTPSConnection")  # Patch the HTTPSConnection class to mock HTTP requests.
    def test_send_telegram_message(self, mock_https_connection):  # Define a test method for sending a Telegram message.
        mock_conn = MagicMock()  # Create a mock connection object.
        mock_https_connection.return_value = mock_conn  # Set the return value of the mocked HTTPSConnection.
        mock_response = MagicMock()  # Create a mock response object.
        mock_response.status = 200  # Set the status code of the mock response.
        mock_response.read.return_value = json.dumps({"ok": True}).encode("utf-8")  # Set the body of the mock response.
        mock_conn.getresponse.return_value = mock_response  # Set the return value of the connection's getresponse method.

        response = self.system.send_telegram_message("Test message")  # Call the method to send a Telegram message.
        self.assertTrue(response["ok"])  # Assert that the response indicates success.
        mock_https_connection.assert_called_once_with("api.telegram.org")  # Assert that the HTTPSConnection was called with the correct host.
        mock_conn.request.assert_called_once_with(  # Assert that the request was made with the correct parameters.
            "POST",
            f"https://api.telegram.org/bot{self.system.bot_token}/sendMessage",
            body=json.dumps({"chat_id": self.system.chat_id, "text": "Test message"}),
            headers={"Content-Type": "application/json"},
        )

    @patch("http.client.HTTPSConnection")  # Patch the HTTPSConnection class to mock HTTP requests.
    def test_send_telegram_frame(self, mock_https_connection):  # Define a test method for sending a Telegram frame.
        mock_conn = MagicMock()  # Create a mock connection object.
        mock_https_connection.return_value = mock_conn  # Set the return value of the mocked HTTPSConnection.
        mock_response = MagicMock()  # Create a mock response object.
        mock_response.status = 200  # Set the status code of the mock response.
        mock_response.read.return_value = json.dumps({"ok": True}).encode("utf-8")  # Set the body of the mock response.
        mock_conn.getresponse.return_value = mock_response  # Set the return value of the connection's getresponse method.

        frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Create a dummy frame.
        response = self.system.send_telegram_frame(frame, "test_frame.jpg")  # Call the method to send a Telegram frame.
        self.assertTrue(response["ok"])  # Assert that the response indicates success.
        mock_https_connection.assert_called_once_with("api.telegram.org")  # Assert that the HTTPSConnection was called with the correct host.
        mock_conn.request.assert_called_once()  # Assert that the request was made.

    @patch.object(SurveillanceSystem, "send_telegram_message")  # Patch the send_telegram_message method of the SurveillanceSystem class.
    @patch.object(SurveillanceSystem, "send_telegram_frame")  # Patch the send_telegram_frame method of the SurveillanceSystem class.
    @patch("concurrent.futures.ThreadPoolExecutor")  # Patch the ThreadPoolExecutor class to mock threading.
    def test_run_telegram_tasks_in_thread(  # Define a test method for running Telegram tasks in a thread.
        self, mock_executor, mock_send_frame, mock_send_message
    ):
        mock_executor_instance = MagicMock()  # Create a mock executor instance.
        mock_executor.return_value = mock_executor_instance  # Set the return value of the mocked ThreadPoolExecutor.

        frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Create a dummy frame.
        self.system.run_telegram_tasks_in_thread("Test message", frame)  # Call the method to run Telegram tasks in a thread.

        mock_executor_instance.submit.assert_called_once()  # Assert that the submit method of the executor was called once.

if __name__ == "__main__":  # Check if the script is being run directly.
    unittest.main()  # Run the unit tests.