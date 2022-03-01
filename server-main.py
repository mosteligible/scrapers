import threading
from DataModels.models import CrawlInitiator
from KijijiScraper.main import run
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/url-list", status_code=301)


@app.get("/crawl/{url}")
async def crawl(url, request: Request):
    print(request.client.host)
    return {"something_to_do": url}


@app.get("/url-list")
async def get_all_urls():
    url_list = [{"path": route.path} for route in app.routes]
    return url_list


@app.post("/scrape")
async def initiate(crawl_init: CrawlInitiator):
    url = crawl_init.url
    num_pages = crawl_init.num_pages
    crawl_thread = threading.Thread(target=run, args=(url, num_pages))
    crawl_thread.daemon = True
    crawl_thread.start()
    return crawl_init
