from WebDriverFactory import WebDriverFactory
import os
import sqlite3
from dotenv import load_dotenv
from ProcessPageJob import ProcessPageJob

load_dotenv()


def main(first_time_run: bool):
    db = sqlite3.connect("wine-ratings.db")

    if first_time_run:
        db.execute(
            """create table reviews (
            seq_no integer primary key autoincrement, 
            page_no integer not null,
            url text not null,
            sha text not null)"""
        )

    driver = WebDriverFactory.create_driver()
    job = ProcessPageJob("https://www.winemag.com/region/us", driver, db)

    root_ratings_url = "https://www.winemag.com/buying-guide/"
    db_start_page = int(os.getenv("DB_START_PAGE"))
    sleep_time = int(os.getenv("SLEEP_TIME"))
    job.run(db_start_page, root_ratings_url, sleep_time)


if __name__ == "__main__":
    main(False)
