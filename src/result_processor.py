import os.path
from typing import Optional, List, Union
import logging
from src.util import json_reader, change_file_extension, text_writer


class ResultProcessor:
    def __init__(self):
        """Initialize ResultProcessor."""
        # Name of the input file
        self.__input_file = None
        # JSON data extracted from the input file
        self.__json_data = None

    def read(self, input_file: str) -> None:
        """Read JSON data from the specified input file.

        Args:
            input_file (str): Path of the input file.
        """
        self.__input_file = input_file
        try:
            self.__json_data = json_reader(input_file)
        except Exception as e:
            logging.error(f"Error reading JSON file {input_file}: {e}")

    def _get_text(self, start: Optional[float] = None, end: Optional[float] = float('inf')) -> str:
        """Extract text from segments between the given start and end times.

        Args:
            start (Optional[float], default=None): Start time.
            end (Optional[float], default=float('inf')): End time.

        Returns:
            str: Extracted text.
        """
        start = float(start)
        end = float(end)
        lines: List[str] = []
        segments = self.__json_data.get("segments")
        if segments is not None:
            for seg in segments:
                text = seg.get("text")
                seg_start = int(seg.get("start"))
                if (start - 0.25) * 60 < seg_start < (end + 0.25) * 60:
                    lines.append(text)

        return "\n".join(lines)

    def output_to_text(self, start: Union[float, str], end: Optional[Union[float, str]] = float('inf'),
                       output_path: str = None) -> str:
        """Convert the content to text and save it as a .txt file.

        Args:
            start (Union[float, str]): Start time.
            end (Optional[Union[float, str]], default=float('inf')): End time.
            output_path (str, optional): Path for the output file.

        Returns:
            str: Name of the output file.
        """
        filename = os.path.basename(self.__input_file)
        if output_path is None:
            output_path = change_file_extension(self.__input_file, ".txt")
        else:
            new_name = change_file_extension(filename, ".txt")
            output_path = os.path.join(output_path, new_name)
        all_text = self._get_text(start, end)
        text_writer(output_path, all_text)

        return filename

    def output_to_srt(self) -> str:
        """Convert the content to SRT format and save as a .srt file.

        Returns:
            str: Name of the output file.
        """
        filename = change_file_extension(self.__input_file, ".srt")
        text_writer(filename, self._get_srt_content())

        return filename

    @staticmethod
    def _format_srt_time(time_in_seconds: int) -> str:
        """Format a timestamp in seconds into the SRT format (HH:MM:SS,MS).

        Args:
            time_in_seconds (int): Timestamp in seconds.

        Returns:
            str: Formatted timestamp.
        """
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)

        return "{:02}:{:02}:{:02},{:03}".format(hours, minutes, seconds, milliseconds)

    def _get_srt_content(self) -> str:
        """Convert the JSON data into SRT formatted content.

        Returns:
            str: Content in SRT format.
        """
        lines: List[str] = []
        segments = self.__json_data.get("segments")
        if segments is not None:
            for i, seg in enumerate(segments, 1):
                text = seg.get("text")
                start = seg.get("start")
                end = seg.get("end")

                # Format timestamps into SRT format
                start_time = self._format_srt_time(start)
                end_time = self._format_srt_time(end)

                lines.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        return "\n".join(lines)
