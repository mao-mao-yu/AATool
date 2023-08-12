from typing import Optional, List, Union
import logging
from src.common import json_reader, change_file_extension, text_writer


class ResultProcessor:
    def __init__(self):
        # Input file name
        self.__input_file = None
        # JSON data from input file
        self.__json_data = None

    def read(self, input_file: str) -> None:
        """
        Read JSON data from input file
        """
        self.__input_file = input_file
        try:
            self.__json_data = json_reader(input_file)
        except Exception as e:
            logging.error(f"Error reading JSON file {input_file}: {e}")

    def _get_text(self, start: Optional[float] = None, end: Optional[float] = float('inf')) -> str:
        """
        Extract text from segments within the specified start and end times
        """
        lines: List[str] = []
        segments = self.__json_data.get("segments")
        if segments is not None:
            for seg in segments:
                text = seg.get("text")
                seg_start = int(seg.get("start"))
                if (start - 0.25) * 60 < seg_start < (end + 0.25) * 60:
                    print(text)
                    lines.append(text)

        return "\n".join(lines)

    def output_to_text(self, start: Union[float, str], end: Optional[Union[float, str]] = float('inf')) -> str:
        """
        Convert content to text and save to a .txt file. Returns the filename.
        """
        filename = change_file_extension(self.__input_file, ".txt")
        all_text = self._get_text(start, end)
        text_writer(filename, all_text)

        return filename

    def output_to_srt(self) -> str:
        """
        Output the text to a .srt file
        """
        filename = change_file_extension(self.__input_file, ".srt")
        text_writer(filename, self._get_srt_content())

        return filename

    @staticmethod
    def _format_srt_time(time_in_seconds: int) -> str:
        """
        Format a timestamp (in seconds) into SRT format (HH:MM:SS,MS)
        """
        hours, remainder = divmod(time_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)

        return "{:02}:{:02}:{:02},{:03}".format(hours, minutes, seconds, milliseconds)

    def _get_srt_content(self) -> str:
        """
        Format the JSON data into SRT content
        """
        lines: List[str] = []
        segments = self.__json_data.get("segments")
        if segments is not None:
            for i, seg in enumerate(segments, 1):
                text = seg.get("text")
                start = seg.get("start")
                end = seg.get("end")

                # format timestamps into SRT format
                start_time = self._format_srt_time(start)
                end_time = self._format_srt_time(end)

                lines.append(f"{i}\n{start_time} --> {end_time}\n{text}\n")
        return "\n".join(lines)
