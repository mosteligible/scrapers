# A python based Scraper to collect advertisement data from Kijiji

A fastapi web server will instantiate scraping job for each request for crawl thats made.

Ideal way is to equate the crawl interval of 1.5 seconds for all the user requesting crawls.

- To spin up the server: `uvicorn server-main:app --host 0.0.0.0`
- Url endpoints are listed at: `/`, `/url-list`
- Crawl is instantiated with POST request at `/scrape` endpoint.

The current implementation requires there be a Database to store the results.

#TODO
- If DB is not there to connect to, save results locally to a file.
