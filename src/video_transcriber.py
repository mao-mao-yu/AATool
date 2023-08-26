import whisper
import logging
import os

from src import const
from src.util import json_writer, change_file_extension, get_file_extension


class VideoTranscriber:
    """
    Class responsible for transcribing audio to text.

    Attributes:
        __model (whisper.Model): Model used for transcription.
        __result (dict): Transcription result.
        __output_directory (str): Directory for the working file.
        __output_path (str): Path for the working file.
        __json_filename (str): Filename of the JSON output.

    Methods:
        transcribe(audio_path: str): Transcribes audio from a given path.
        output_to_file(output_path: str = None): Saves transcription result to a file.
        is_support_audio(filename: str): Checks if file is supported audio.
        is_support_video(filename: str): Checks if file is supported video.
    """

    def __init__(self, model_name="medium"):
        """
        Initialize the VideoTranscriber object.

        Parameters:
            model_name (str): Name of the whisper model to be loaded. Default is "medium".
        """
        try:
            self.__model = whisper.load_model(model_name)
        except Exception as e:
            logging.error(f"Model loading error: {e}")
            raise e
        self.__result = None
        self.__output_directory = None
        self.__output_path = None
        self.__json_filename = None

    def transcribe(self, audio_path: str) -> 'VideoTranscriber':
        """
        Transcribe audio from a given path.

        Parameters:
            audio_path (str): Path to the audio file.

        Returns:
            VideoTranscriber: Current instance of VideoTranscriber.
        """
        try:
            self.__result = self.__model.transcribe(audio_path)
            logging.debug("Transcribed audio...")
        except Exception as e:
            logging.error(f"Audio to text error: {e}")
            raise e

        self.__output_directory = os.path.dirname(audio_path)
        self.__json_filename = change_file_extension(os.path.basename(audio_path), ".json")
        self.__output_path = os.path.join(self.__output_directory, self.__json_filename)
        logging.debug(f"Set output directory to {self.__output_directory} and output path to {self.__output_path}...")

        return self

    def output_to_file(self, output_path: str = None) -> str:
        """
        Save the transcription result to a file.

        Parameters:
            output_path (str, optional): Path for the work file. Uses path from transcription if not provided.

        Returns:
            str: Path where the result was saved.
        """
        if output_path is not None:
            self.__output_path = os.path.join(output_path, self.__json_filename)

        try:
            json_writer(self.__output_path, self.__result)
            logging.info(f"Saved result to {self.__output_path}...")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")
            raise e

        return self.__output_path

    @staticmethod
    def is_support_audio(filename):
        """Determine if the provided file is a supported audio format."""
        return get_file_extension(filename) in const.support_audio

    @staticmethod
    def is_support_video(filename):
        """Determine if the provided file is a supported video format."""
        return get_file_extension(filename) in const.support_video
