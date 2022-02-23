from fastapi import FastAPI
from DataModels.models import CrawlInitiator


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/crawl/{url}")
async def crawl(url):
    return {"something_to_do": url}


@app.post("/scrape")
async def initiate(crawl_init: CrawlInitiator):
    return crawl_init
