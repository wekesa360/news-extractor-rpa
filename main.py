from src.news_extractor_process import NewsExtractorProcess
from robocorp.tasks import task


def news_extractor_process_task():
    news_extractor = NewsExtractorProcess()
    news_extractor.run_news_extractor()

if __name__ == "__main__":
    news_extractor_process_task()