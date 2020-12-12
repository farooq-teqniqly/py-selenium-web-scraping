from WebDriverFactory import WebDriverFactory
import os
import sqlite3
from dotenv import load_dotenv
from ProcessPageJob import ProcessPageJob

load_dotenv()


def main():
    root_ratings_url = "https://www.winemag.com/buying-guide/"
    create_db_table_str = os.getenv("CREATE_DB_TABLE")
    db_start_page_str = os.getenv("DB_START_PAGE")
    sleep_time_str = os.getenv("SLEEP_TIME")

    create_db_table = 0
    db_start_page = 1
    sleep_time = 2

    driver = WebDriverFactory.create_driver()
    db = sqlite3.connect("wine-ratings.db")
    job = ProcessPageJob("https://www.winemag.com/region/us", driver, db)

    if create_db_table_str:
        create_db_table = int(create_db_table_str)

    if create_db_table == 1:
        db.execute(
            """create table reviews (
            seq_no integer primary key autoincrement, 
            page_no integer not null,
            url text not null,
            sha text not null)"""
        )

    if db_start_page_str:
        db_start_page = int(db_start_page_str)

    if sleep_time_str:
        sleep_time = int(sleep_time_str)

    job.run(db_start_page, root_ratings_url, sleep_time)


if __name__ == "__main__":
    main()
