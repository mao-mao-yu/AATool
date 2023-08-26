import logging
import os
from src import util, const, config


class ToolScheduler:
    """Initialize and manage the tool scheduler."""

    def __init__(self, video_transcriber, result_processor):
        """Constructor for the ToolScheduler class."""

        # Initialize video transcriber and result processor instances
        self.video_transcriber = video_transcriber
        self.result_processor = result_processor

        # Set initial values for configuration attributes
        self.input_file = None
        self.start = None
        self.end = None
        self.output_folder = None
        self.work_directory = self.get_work_folder()

        # Initialize the configuration settings
        self.init_config()

    def run(self):
        """Process all supported files in the given directory or process a single file."""

        if os.path.isdir(self.input_file):
            for file in os.listdir(self.input_file):
                if self.video_transcriber.is_support_audio(file):
                    self.process(file)
        else:
            self.process(self.input_file)

    def init_config(self):
        """Configure logging settings and read configurations from arguments."""

        config.configure_logging()
        self.input_file, self.start, self.end, self.output_folder = config.read_config_args()
        if self.start == "":
            self.start = 0.0
        if self.end == "":
            self.end = float('inf')

    @staticmethod
    def get_work_folder():
        """Retrieve the working directory path."""

        return os.path.join(os.getcwd(), "work")

    def get_output_folder(self, input_path: str) -> str:
        """Determine the output folder based on input file and configuration."""

        if self.output_folder is not None and self.output_folder != "":
            # If output folder is defined, use it and ensure it exists
            output_folder = os.path.abspath(self.output_folder)
            util.ensure_directory_exists(output_folder)
        else:
            # Use input's directory as output or its parent directory
            if os.path.isdir(input_path):
                output_folder = input_path
            else:
                output_folder = os.path.dirname(os.path.abspath(input_path))

        return output_folder

    def process(self, input_file):
        """Determine the input file type and process accordingly."""
        logging.debug(f"Start process {input_file}")
        file_extension = self.get_supported_file_extension(input_file)
        if file_extension is None:
            logging.error(f"FFMPEG does not support this type...{input_file}")
            return

        # Check file extension and process video, audio or JSON files
        if file_extension in const.support_video:
            self.process_video(input_file)
        elif file_extension in const.support_audio:
            self.process_audio(input_file)
        elif file_extension.lower() == ".json":
            output_path = self.get_output_folder(input_file)
            self.process_json(input_file, output_path)
        else:
            logging.error(f"Error file type {input_file}")

    def process_video(self, input_path):
        """Convert video format files to audio format."""

        logging.info("Starting to convert video to audio")
        input_path = util.video_to_audio(input_path, self.work_directory)
        self.process_audio(input_path)

    def process_audio(self, input_path):
        """Transcribe audio files into a JSON format."""

        input_path = self.video_transcriber.transcribe(input_path).output_to_file(self.work_directory)
        self.process_json(input_path, self.get_output_folder(self.input_file))

    def process_json(self, json_filepath, output_folder):
        """Read the JSON content and convert to text format."""

        self.result_processor.read(json_filepath)
        self.result_processor.output_to_text(self.start, self.end, output_folder)
        logging.info(f"Converted to TXT file in {output_folder}")

    def get_supported_file_extension(self, filepath):
        """Check if the filepath is of a supported file type and return its extension."""

        if self.video_transcriber.is_support_video(filepath) or self.video_transcriber.is_support_video(
                filepath) or filepath.lower().endswith(".json"):
            return util.get_file_extension(filepath)
