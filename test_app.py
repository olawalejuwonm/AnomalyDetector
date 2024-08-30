import unittest  # Import the unittest module for creating and running tests.
import os  # Import the os module for interacting with the operating system.
from unittest.mock import patch, MagicMock  # Import patch and MagicMock for mocking dependencies.
from app import app, start_flask  # Import the Flask app and start_flask function from the app module.

class TestApp(unittest.TestCase):  # Define a test case class inheriting from unittest.TestCase.

    def setUp(self):  # Define the setup method to initialize the test client.
        self.app = app.test_client()  # Create a test client for the Flask app.
        self.app.testing = True  # Enable testing mode for the Flask app.

    @patch("app.get_video_files")  # Mock the get_video_files function in the app module.
    def test_check_videos(self, mock_get_video_files):  # Define a test method for the /check-videos endpoint.
        mock_get_video_files.return_value = (  # Set the return value of the mocked get_video_files function.
            os.path.join(app.static_folder, "recorded_videos"),  # Return the path to the recorded videos folder.
            ["video1.webm"],  # Return a list containing one video file.
        )

        response = self.app.get("/check-videos")  # Send a GET request to the /check-videos endpoint.

        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200.
        self.assertEqual(response.json, ["video1.webm"])  # Assert that the response JSON contains the expected video file.

    @patch("os.path.exists")  # Mock the os.path.exists function.
    @patch("os.remove")  # Mock the os.remove function.
    def test_delete_video(self, mock_remove, mock_exists):  # Define a test method for the /delete-video endpoint.
        mock_exists.side_effect = lambda x: x.endswith("video1.webm") or x.endswith(  # Set the side effect of the mocked os.path.exists function.
            "video1.webm.json"  # Return True if the file name ends with video1.webm or video1.webm.json.
        )

        response = self.app.post("/delete-video", json={"file_name": "video1.webm"})  # Send a POST request to the /delete-video endpoint with the file name.

        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200.
        self.assertEqual(response.json, {"success": "video1.webm deleted successfully"})  # Assert that the response JSON contains the expected success message.
        mock_remove.assert_called()  # Assert that the os.remove function was called.

    @patch("subprocess.run")  # Mock the subprocess.run function.
    def test_run_main(self, mock_run):  # Define a test method for the /run-main endpoint.
        mock_run.return_value = MagicMock(stdout="Script output", stderr="")  # Set the return value of the mocked subprocess.run function.

        response = self.app.post("/run-main")  # Send a POST request to the /run-main endpoint.

        self.assertEqual(response.status_code, 200)  # Assert that the response status code is 200.

    @patch("waitress.serve")  # Mock the waitress.serve function.
    @patch("app.app.run")  # Mock the app.run function in the app module.
    def test_start_flask(self, mock_run, mock_serve):  # Define a test method for the start_flask function.
        start_flask(app=app, port=5000, host="0.0.0.0")  # Call the start_flask function with the app, port, and host.

        mock_serve.assert_called_once_with(app, port=5000, host="0.0.0.0")  # Assert that the waitress.serve function was called with the correct arguments.
        mock_run.assert_not_called()  # Assert that the app.run function was not called.

if __name__ == "__main__":  # Check if the script is being run directly.
    unittest.main()  # Run the unit tests.