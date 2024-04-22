# News Extractor Process

The News Extractor Process is a Python-based automation tool that extracts news articles from a website based on a given search phrase, news category, and date range. This process is designed to be used as part of a larger robotic process automation (RPA) workflow.

## Features
- Retrieves news articles from a specified website based on a search phrase, news category, and date range
- Extracts relevant data from the articles, including title, date, description, and image URL
- Filters the articles based on the specified news category and date range
- Tracks the count of the search phrase in the article text
- Checks if the article contains any mention of money
- Downloads the article images and saves them to the output directory
- Writes the extracted article data to an Excel file

## Requirements
- Python 3.7 or higher
- The following Python libraries:
 - `robocorp`
 - `datetime`
 - `dotenv` # for reading environment variables from a .env file in test or local environments for the `RC_WORKITEM_INPUT_PATH`
 - `openpyxl`

## Usage
1. Ensure that all the required dependencies are installed.
2. Create a `.env` file in the project directory and add the following line:
    ```
    RC_WORKITEM_INPUT_PATH=<path_to_input_file>
    ```
This sets the path for the work item input file, which is used for testing purposes.
3. Create a `config.yaml` file in the project directory and add the following configuration values, a fallback for the work items input or default configs:
```yaml
website_url: https://www.example.com
search_phrase: "example search phrase"
news_category: "politics"
num_months: 3
```
These values will be used as fallback options if the work item input does not contain the required information.
4. Run `main.py` to execute the news extraction process.

**How It Works**
----------------

1.  The `NewsExtractorProcess` class is initialized with the necessary dependencies, such as the `ConfigManager`, `LoggingManager`, `BrowserAutomator`, `ImageDownloader`, and `ExcelExporter`.
   
2.  The `run_news_extractor()` method is called to execute the news extraction process.
   
3.  The method retrieves the configuration values for the website URL, search phrase, news category, and number of months from either the work item input or the `config.yaml` file.
   
4.  The browser is opened, and the specified website is navigated to.
   
5.  The search phrase is entered into the search field, and the article elements are found on the page.
   
6.  The method iterates over the article elements, extracting the relevant data (title, date, description, and image URL) and performing additional checks:
   
   *   Checks if the article is in the specified news category.
       
   *   Checks if the article is within the specified date range.
       
   *   Updates the search phrase count in the article data.
       
   *   Checks if the article contains any mention of money.
       
   *   Downloads the article image and stores the filename.
       
7.  The extracted article data is written to an Excel file in the `output/` directory.
   
8.  Finally, the browser is closed, and the process is completed.
   

**Logging and Error Handling**
------------------------------

The `NewsExtractorProcess` class uses the `LoggingManager` to log various events and errors that occur during the process. The logs are written to the `output/news_extractor.log` file.

If any errors occur during the process, they are logged, and the browser is closed to ensure a clean state for the next execution.
