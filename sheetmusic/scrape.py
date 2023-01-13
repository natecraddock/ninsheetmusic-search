"""
scrape sheet music data from www.ninsheetmusic.org
"""

import datetime
import logging
import os
import requests
from bs4 import BeautifulSoup

# the series page is the easiest to scrape
BASE_URL = "https://www.ninsheetmusic.org"
SERIES_URL = f"{BASE_URL}/browse/series"

def timestamp() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def scrape():
    """
    Scrape all data and output as json to stdout
    """

    logging.info(f"started scraping ninsheetmusic.org")

    sheets = scrape_all_series()
    if not sheets:
        logging.warn(f"unable to scrape ninsheetmusic.org for data")
        return

    data = { "sheets": sheets, "timestamp": timestamp() }

    logging.info(f"finished scraping")

    return data

def scrape_all_series() -> list:
    """
    Iterate through each series page
    """
    r = requests.get(SERIES_URL)
    if not r.ok:
        return []

    series_page = BeautifulSoup(r.text, "html.parser")
    categories = series_page.select(".browseCategoryList a")
    categories = [c.attrs["href"] for c in categories]

    # iterate over each series
    all_sheets = []
    for c in categories:
        sheets = scrape_series_page(f"{SERIES_URL}/{os.path.basename(c)}")
        all_sheets.extend(sheets)

    return all_sheets

def scrape_series_page(url: str) -> list:
    """
    Scrape data for each game in a series
    """
    r = requests.get(url)
    if not r.ok:
        return []

    page = BeautifulSoup(r.text, "html.parser")

    # get series title
    series_name = list(page.select_one("#mainTitle span").stripped_strings)[0]

    # iterate over each game in the series
    series_sheets = []
    games = page.select(".game")
    for game in games:
        game_title = game.select_one("heading h3").text.strip()
        platform = game.select_one(".consoleList a").text.strip()
        sheets = game.select(".tableList li")
        for sheet in sheets:
            series_sheets.append(scrape_sheet_data(series_name, game_title, platform, sheet))

    return series_sheets

def scrape_sheet_data(series_name: str, game_title: str, platform: str, sheet) -> dict:
    """
    Combine all data for a sheet into a single dict
    """
    title = sheet.select_one(".tableList-cell--sheetTitle").text.strip()
    pdf = sheet.select_one(".tableList-buttonCell--sheetPdf").attrs["href"].strip()
    pdf = f"{BASE_URL}{pdf}"

    # Keep order the same as the sqlite schema
    return (
        title,
        game_title,
        series_name,
        platform,
        pdf,
    )

if __name__ == "__main__":
    scrape()
