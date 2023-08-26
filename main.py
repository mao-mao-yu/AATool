from src.video_transcriber import VideoTranscriber
from src.result_processor import ResultProcessor
from src.tool_scheduler import ToolScheduler


def main():
    vt = VideoTranscriber()
    rp = ResultProcessor()
    ts = ToolScheduler(vt, rp)
    ts.run()
    input("Enter to quit")


if __name__ == '__main__':
    main()
