import logging
import os.path
import sys
import configparser

from src import video_transcriber, result_processor, common, const
import argparse


def configure_logging():
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，将日志写入文件
    file_handler = logging.FileHandler('./log/ATTool.log', mode='a', encoding="utf8")
    file_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器，将日志输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # 定义日志消息格式
    formatter = logging.Formatter('[%(asctime)s - %(levelname)s] : %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 将处理器添加到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def cmd_args():
    parser = argparse.ArgumentParser(description="视频剪辑工具")

    # 添加命令行参数
    parser.add_argument("-i", "--input", type=str, required=True, help="输入视频文件路径")
    parser.add_argument("-s", "--start_time", default=0, type=float, help="开始时间（浮点数格式）")
    parser.add_argument("-e", "--end_time", default=float("inf"), type=float, help="结束时间（浮点数格式）")
    parser.add_argument("-o", "--output_folder", default=r"./output", type=str, help="输出文件夹路径")

    args = parser.parse_args()

    return args.input, args.start_time, args.end_time, args.output_folder


def ini_args():
    config = configparser.ConfigParser()
    config.read('./setting.ini', encoding="utf8")

    # 读取某个部分的某个值
    settings = config['SETTINGS']
    return settings['input'], settings['start'], settings['end'], settings['output']


def main():
    # 日志初始化
    configure_logging()
    # args
    # input_video_path, start, end, output_folder = cmd_args()
    input_video_path, start, end, output_folder = ini_args()

    if os.path.isdir(input_video_path):
        logging.error("输入的不是文件")

    file_extensions = common.get_file_extension(input_video_path)

    # 是否是支持的格式
    if file_extensions not in const.video_formats and file_extensions not in const.audio_formats:
        logging.error(f"不支持的格式{file_extensions}")

    # 判断输出文件夹路径
    if output_folder is not None:
        output_folder = os.path.abspath(output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        # 使用默认输出文件夹路径：视频文件所在文件夹
        output_folder = os.path.dirname(os.path.abspath(input_video_path))

    # 如果是视频则转音频
    if file_extensions in const.video_formats:
        logging.info("开始转换视频到音频")
        audio_path = common.video_to_audio(input_video_path, output_folder)
    else:
        audio_path = input_video_path

    logging.info("开始抄录音频到json")
    vt = video_transcriber.VideoTranscriber()
    json_path = vt.transcribe(audio_path).output_to_file(output_folder)
    logging.info(f"已抄录到{json_path}")

    rp = result_processor.ResultProcessor()
    rp.read(json_path)
    rp.output_to_text(start, end)
    logging.info(f"已转换为TXT文件到{output_folder}")
    input("输入任意键退出")


if __name__ == '__main__':
    main()
