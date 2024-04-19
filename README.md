# News Extractor

News Extractor is a Python application that extracts news articles from a website(NewYork Times) based on a search phrase and a specified news category. It downloads article images, counts the occurrences of the search phrase in the article content, checks for mentions of money-related information, and exports the extracted data to an Excel file.

## Features

- Performs a search on a given website and retrieves news article results
- Filters articles based on a specified news category
- Extracts article data (title, date, description, image URL)
- Downloads article images and saves them locally
- Counts the occurrences of the search phrase in the article content
- Checks if the article contains money-related information
- Exports the extracted data (article details, search phrase count, money mention) to an Excel file

## Requirements

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:
`git@github.com:wekesa360/news-extractor-rpa.git`
2. Navigate to the project directory:
`cd news-extractor`

3. Install the required packages:
`pip install -r requirements.txt`

## Configuration

1. Create a `config` directory in the project root.
2. Create a `config.yaml` file in the `config` directory.
3. Add the following configuration parameters to the `config.yaml` file:

```yaml
website_url: "https://www.nytimes.com"
search_phrase: "your search phrase"
news_category: "Technology"
num_months: 6
```