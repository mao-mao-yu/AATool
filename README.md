
# ATTool 音视频转录工具 (ATTool Audio and Video Transcription Tool)  
![日本語](https://github.com/mao-mao-yu/AATool/blob/master/README_JP.md)

## 描述 (Description)

这是一个用于音视频转录的工具，可以将音频和视频文件转换为文本。  
(This is a tool for audio and video transcription, capable of converting audio and video files into text.)

## 文件说明 (File Descriptions)

### 1. video_transcriber.py (音频转录)

此文件定义了一个名为 `VideoTranscriber` 的类，用于将音频转录为文本。它使用了 `whisper` 模块进行转录。  
(This file defines a class named `VideoTranscriber` that is used to transcribe audio into text. It uses the `whisper` module for transcription.)

### 2. result_processor.py (转录结果处理)

此文件定义了一个名为 `ResultProcessor` 的类，用于处理并读取转录结果的JSON文件。  
(This file defines a class named `ResultProcessor` that is used to handle and read transcription results from a JSON file.)

### 3. main.py (主程序)

这是工具的主要执行文件，它配置了日志记录器，包含命令行参数，并定义了主要的程序执行逻辑。  
(This is the main execution file for the tool. It sets up a logger, contains command-line arguments, and defines the main program execution logic.)

### 4. const.py (常量定义)

此文件定义了工具支持的音频和视频格式。  
(This file defines the audio and video formats supported by the tool.)

### 5. common.py (常用功能)

这个文件包含了一些常用的功能函数，例如将内容写入JSON文件的函数。  
(This file contains common utility functions, like the one used for writing content into a JSON file.)

## 使用方法 (Usage)

请根据 `main.py` 中的命令行参数说明或者配置文件来使用此工具。  
(Please refer to the command-line argument descriptions in `main.py` for usage instructions.)

