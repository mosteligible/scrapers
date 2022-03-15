from DataModels.models import CrawlInitiator
from KijijiScraper.utils import validate_url
from KijijiScraper import LongtermRentals
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/url-list", status_code=301)


@app.get("/url-list")
async def get_all_urls(request: Request):
    ip_address = request.client.host
    url_list = [{"path": route.path} for route in app.routes]
    url_list.append({"ip_address": ip_address})
    return url_list


@app.post("/scrape")
async def initiate(crawl_init: CrawlInitiator, request: Request):
    url = crawl_init.url
    num_pages = crawl_init.num_pages
    ip_addr = request.client.host
    if not validate_url(url=url):
        return {"message": "Error, url provided is invalid!"}
    crawl_thread = LongtermRentals(url=url, num_pages=num_pages, ip_addr=ip_addr)
    crawl_thread.daemon = True
    crawl_thread.start()
    return ip_addr, num_pages
