import os
import subprocess
import logging
import json
from typing import Any, Optional


def json_writer(output_file: str,
                content: Any,
                encoding: str = "utf-8",
                indent: int = 2,
                ensure_ascii: bool = False) -> None:
    """Write `content` to `output_file` in JSON format.

    Args:
        output_file (str): The path of the file to write to.
        content (Any): The content to be written to the file.
        encoding (str, optional): The encoding to use when writing the file. Defaults to "utf-8".
        indent (int, optional): The number of spaces for indentation of nested structures. Defaults to 2.
        ensure_ascii (bool, optional): If True, the output is guaranteed to be ASCII. Defaults to False.
    """
    try:
        with open(output_file, 'w', encoding=encoding) as f:
            json.dump(content, f, indent=indent, ensure_ascii=ensure_ascii)
        logging.debug(f"Writen to {output_file}...")
    except Exception as e:
        logging.error(f"Failed to write to {output_file}: {e}")
        raise RuntimeError(f"Failed to write to {output_file}: {e}") from e


def text_writer(output_file: str,
                content: str,
                encoding: str = "utf-8",
                is_overwrite: bool = True) -> None:
    if os.path.exists(output_file) and not is_overwrite:
        logging.error(f"File already exists: {output_file}")
        return
    try:
        with open(output_file, 'w', encoding=encoding) as f:
            f.write(content)
        logging.debug(f"Wrote to file {output_file}")
    except Exception as e:
        logging.error(f"Failed to write to {output_file}: {e}")
        raise RuntimeError(f"Failed to write to {output_file}: {e}") from e


def json_reader(input_file: str, encoding: str = "utf-8") -> dict:
    """Read a JSON file and return the content as a Python dictionary.

    Args:
        input_file (str): The path of the JSON file to read.
        encoding (str, optional): The encoding to use when reading the file. Defaults to "utf-8".

    Returns:
        dict: The content of the JSON file as a Python dictionary.
    """
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            data = json.load(f)
        logging.debug(f"Loaded json from {input_file}...")
        return data
    except Exception as e:
        logging.error(f"Failed to read from {input_file}: {e}")
        raise RuntimeError(f"Failed to read from {input_file}: {e}") from e


def video_to_audio(input_file: str,
                   output_dir: str,
                   audio_codec: str = "aac",
                   start: Optional[str] = None,
                   end: Optional[str] = None) -> str:
    try:
        filename = os.path.basename(input_file).split(".")[0] + "." + audio_codec
        output_file = os.path.join(output_dir, filename)

        command = [
            "ffmpeg",
            "-i", input_file,
            "-vn",
            "-c:a",
            audio_codec,
            output_file
        ]

        # 如果提供了开始时间和结束时间，将它们添加到命令中
        if start:
            command.extend(["-ss", start])
        if end:
            command.extend(["-to", end])

        command.append(output_file)

        subprocess.run(command, check=True)
        logging.debug("Video to audio conversion successful!")
        return output_file

    except subprocess.CalledProcessError as e:
        logging.error(f"Video to audio conversion failed: {e}")
        raise subprocess.CalledProcessError(f"Video to audio conversion failed: {e}") from e


def change_file_extension(old_path: str, new_extension: str) -> str:
    """Change the file extension of a file.

    Args:
        old_path (str): The old file path.
        new_extension (str): The new file extension.

    Returns:
        str: The new file path.
    """
    file_name, old_extension = os.path.splitext(old_path)
    new_filename = file_name + new_extension

    return new_filename


def get_file_extension(file_path):
    # 使用os.path.splitext()函数获取文件扩展名
    _, extension = os.path.splitext(file_path)
    return extension
