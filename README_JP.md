# Whisperを使ったSTT(Speech to text)ツール  
OpenaiのWhisperがサポートする言語音声をテキストにすることができます

setting.iniにビデオや音声ファイルのデータとstart,end時間と出力パスを入れてstart.batを起動します。
CPUも使えますが、GPUのほうが早いです。

# ATTool 音声・映像の転写ツール
*(ATTool Audio and Video Transcription Tool)*

## 説明
*(Description)*

これは音声および映像の転写ツールで、音声と映像ファイルをテキストに変換することができます。  
*(This is a tool for audio and video transcription, capable of converting audio and video files into text.)*

## ファイル説明
*(File Descriptions)*

### 1. video_transcriber.py *(音声転写)*
このファイルには、音声をテキストに転写するための `VideoTranscriber` というクラスが定義されています。転写のために `whisper` モジュールを使用しています。  
*(This file defines a class named `VideoTranscriber` that is used to transcribe audio into text. It uses the `whisper` module for transcription.)*

### 2. result_processor.py *(転写結果の処理)*
このファイルには、転写結果のJSONファイルを処理および読み取るための `ResultProcessor` というクラスが定義されています。  
*(This file defines a class named `ResultProcessor` that is used to handle and read transcription results from a JSON file.)*

### 3. main.py *(メインプログラム)*
これはツールの主要な実行ファイルです。ロガーを設定し、コマンドラインの引数を含み、主要なプログラムの実行ロジックを定義しています。  
*(This is the main execution file for the tool. It sets up a logger, contains command-line arguments, and defines the main program execution logic.)*

### 4. const.py *(定数定義)*
このファイルには、ツールがサポートする音声および映像のフォーマットが定義されています。  
*(This file defines the audio and video formats supported by the tool.)*

### 5. common.py *(一般的な機能)*
このファイルには、JSONファイルにコンテンツを書き込むための関数など、一般的なユーティリティ関数が含まれています。  
*(This file contains common utility functions, like the one used for writing content into a JSON file.)*

## 使い方
*(Usage)*

`main.py` に記載されているコマンドラインの引数の説明または設定ファイルを参照して、このツールを使用してください。  
*(Please refer to the command-line argument descriptions in `main.py` for usage instructions.)*
