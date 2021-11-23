import argparse
import logging

from fetch.scrape import fetch_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", 
        "--file", 
        help="include roll numbers from file(see readme.md)",
        nargs="?",
        const="rolls.txt"
        )
    
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting")
    fetch_results()
    logging.info("Finished")
    


if __name__ == "__main__":
    main()