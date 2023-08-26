import os
import subprocess
import logging
import json
from typing import Any, Optional
import src.const


def json_writer(output_file: str, content: Any, encoding: str = "utf-8", indent: int = 2,
                ensure_ascii: bool = False) -> None:
    """Write content to a file in JSON format.

    Args:
        output_file (str): Path of the file to write to.
        content (Any): Content to write to the file.
        encoding (str, optional): Encoding for writing to the file. Defaults to "utf-8".
        indent (int, optional): Indentation level for nested structures. Defaults to 2.
        ensure_ascii (bool, optional): Ensure written content is ASCII. Defaults to False.
    """
    try:
        with open(output_file, 'w', encoding=encoding) as f:
            json.dump(content, f, indent=indent, ensure_ascii=ensure_ascii)
        logging.debug(f"Wrote to {output_file}...")
    except Exception as e:
        logging.error(f"Failed writing to {output_file}: {e}")
        raise RuntimeError(f"Failed writing to {output_file}: {e}") from e


def text_writer(output_file: str, content: str, encoding: str = "utf-8", is_overwrite: bool = True) -> None:
    """Write text content to a file.

    Args:
        output_file (str): Path of the file to write to.
        content (str): Text content to write to the file.
        encoding (str, optional): Encoding for writing to the file. Defaults to "utf-8".
        is_overwrite (bool, optional): Overwrite if file exists. Defaults to True.
    """
    if os.path.exists(output_file) and not is_overwrite:
        logging.error(f"File {output_file} already exists.")
        return
    try:
        with open(output_file, 'w', encoding=encoding) as f:
            f.write(content)
        logging.debug(f"Wrote to file {output_file}")
    except Exception as e:
        logging.error(f"Failed writing to {output_file}: {e}")
        raise RuntimeError(f"Failed writing to {output_file}: {e}") from e


def json_reader(input_file: str, encoding: str = "utf-8") -> dict:
    """Read and return content from a JSON file.

    Args:
        input_file (str): Path of the JSON file to read.
        encoding (str, optional): Encoding for reading the file. Defaults to "utf-8".

    Returns:
        dict: Content of the JSON file.
    """
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            data = json.load(f)
        logging.debug(f"Read data from {input_file}...")
        return data
    except Exception as e:
        logging.error(f"Failed reading from {input_file}: {e}")
        raise RuntimeError(f"Failed reading from {input_file}: {e}") from e


def ensure_directory_exists(directory_path):
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def video_to_audio(input_file: str, output_dir: str, audio_codec: str = "aac", start: Optional[str] = None,
                   end: Optional[str] = None) -> str:
    """Convert video to audio.

    Args:
        input_file (str): Path of the video file.
        output_dir (str): Output directory for the audio file.
        audio_codec (str, optional): Audio codec to use. Defaults to "aac".
        start (str, optional): Start time for conversion. Defaults to None.
        end (str, optional): End time for conversion. Defaults to None.

    Returns:
        str: Path of the converted audio file.
    """
    try:
        filename = os.path.basename(input_file).split(".")[0] + "." + audio_codec
        output_file = os.path.join(output_dir, filename)
        command = ["ffmpeg", "-i", input_file, "-vn", "-c:a", audio_codec, output_file, "-y"]
        if start:
            command.extend(["-ss", start])
        if end:
            command.extend(["-to", end])
        command.append(output_file)
        subprocess.run(command, check=True)
        logging.debug("Video to audio conversion successful!")
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Video to audio conversion error: {e}")
        raise subprocess.CalledProcessError(f"Video to audio conversion error: {e}") from e


def change_file_extension(old_path: str, new_extension: str) -> str:
    """Change file extension.

    Args:
        old_path (str): Original file path.
        new_extension (str): New file extension to set.

    Returns:
        str: New file path.
    """
    file_name, _ = os.path.splitext(old_path)
    new_filename = file_name + new_extension
    return new_filename


def get_file_extension(file_path: str) -> str:
    """Retrieve file extension from a file path.

    Args:
        file_path (str): Path of the file.

    Returns:
        str: File extension.
    """
    _, extension = os.path.splitext(file_path)
    return extension
