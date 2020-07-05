import requests
import json


def main():
    res = requests.get (" https://www.goodreads.com/book/review_counts.json", params =
    {" key ":"dZGnlkLsiELtLnSrHQThzA", "isbns": "0743269268"})
    data = res.json()
    print(data)
    for book in data['books']:
        print('isbn13:', book['isbn13'])
        print('work_ratings_count:', book['work_ratings_count'])
        print('')


if __name__ == "__main__":
    main()