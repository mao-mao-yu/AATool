import whisper
import logging
import os
from src.common import json_writer, change_file_extension


class VideoTranscriber:
    """
    A class used to transcribe audio to text.

    Attributes:
    __model (whisper.Model): The whisper model used for transcription.
    __result (dict): The transcription result.
    __output_directory (str): The directory of the output file.
    __output_path (str): The path of the output file.

    Methods:
    transcribe(audio_path: str): Transcribes the audio at the specified path.
    output_to_file(output_path: str = None): Writes the transcription result to a file.
    """

    def __init__(self, model_name="medium"):
        """
        Constructs all the necessary attributes for the VideoTranscriber object.

        Parameters:
        model_name (str): The name of the whisper model to load. Defaults to "medium".
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
        Transcribes the audio at the specified path.

        Parameters:
        audio_path (str): The path of the audio file to transcribe.

        Returns:
        self (VideoTranscriber): The instance of the VideoTranscriber.
        """
        try:
            self.__result = self.__model.transcribe(audio_path)
            logging.debug(f"Transcribed audio...")
        except Exception as e:
            logging.error(f"Audio to text error: {e}")
            raise e

        self.__output_directory = os.path.dirname(audio_path)
        self.__json_filename = change_file_extension(os.path.basename(audio_path), ".json")
        self.__output_path = os.path.join(self.__output_directory, self.__json_filename)
        logging.debug(f"Set output_directory {self.__output_directory} and output_path {self.__output_path}...")

        return self

    def output_to_file(self, output_path: str = None) -> str:
        """
        Writes the transcription result to a file.

        Parameters:
        output_path (str, optional): The path of the output file. If not specified, uses the path set during transcription.
        """
        if output_path is not None:
            self.__output_path = os.path.join(output_path, self.__json_filename)

        try:
            json_writer(self.__output_path, self.__result)
            logging.info(f"Saved result to {self.__output_path}...")
        except Exception as e:
            logging.error(f"Writing to file error: {e}")
            raise e

        return self.__output_path
