import requests


def main():
    res = requests.get (" https://www.goodreads.com/book/review_counts.json", params =
    {" key ":"dZGnlkLsiELtLnSrHQThzA", "isbns": "0743269268"})
    print (res.text)

if __name__ == "__main__":
    main()