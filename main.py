from src.news_extractor_process import NewsExtractorProcess
from robocorp.tasks import task

@task
def news_extractor_process_task():
    news_extractor = NewsExtractorProcess()
    news_extractor.run_news_extractor()
