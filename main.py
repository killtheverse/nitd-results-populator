import argparse
import logging

from getpass import getpass
from dotenv import load_dotenv
from fetch.scrape import fetch_results
from client.apiclient import APIClient


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b",
        "--browser",
        help="browser specification for web scraping",
        default="firefox",
        choices=["chrome", "firefox", "edge", "safari"]
    )
    parser.add_argument(
        "-d",
        "--driver",
        help="path to the driver",
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")
    username = input("Username:")
    password = getpass("Password:")
    creds = {
        "username": username,
        "password": password
    }
    client = APIClient(creds)
    fetch_results(args.browser, args.driver, client)
    logging.info("Finished")


if __name__ == "__main__":
    main()
    