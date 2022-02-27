import threading
from DataModels.models import CrawlInitiator
from KijijiScraper.main import run
from fastapi import FastAPI, Request


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/crawl/{url}")
async def crawl(url, request: Request):
    print(request.client.host)
    return {"something_to_do": url}


@app.post("/scrape")
async def initiate(crawl_init: CrawlInitiator):
    url = crawl_init.url
    num_pages = crawl_init.num_pages
    crawl_thread = threading.Thread(target=run, args=(url, num_pages))
    crawl_thread.daemon = True
    crawl_thread.start()
    return crawl_init
