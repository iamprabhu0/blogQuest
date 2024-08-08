import argparse
import sqlite3
from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run
import pathlib

script_dir = pathlib.Path(__file__).resolve().parent
templates_path = script_dir / "templates"
static_path = script_dir / "static"

app = FastAPI()
templates = Jinja2Templates(directory=str(templates_path))
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

class SearchEngine:
    def __init__(self, db_path):
        self.db_path = db_path

    def search(self, query, n=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT url, bm25(feeds) as score 
            FROM feeds 
            WHERE feeds MATCH ? 
            ORDER BY score LIMIT ?;
        """, (query, n))
        results = cursor.fetchall()
        conn.close()
        return results

def get_top_urls(results):
    return {url: score for url, score in results}

@app.on_event("startup")
async def startup_event():
    args = parse_args()
    app.state.engine = SearchEngine(args.db_path)

@app.get("/", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/results/{query}", response_class=HTMLResponse)
async def search_results(request: Request, query: str = Path(...)):
    results = app.state.engine.search(query)
    results = get_top_urls(results)
    return templates.TemplateResponse("results.html", {"request": request, "results": results, "query": query})


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default="feeds.db")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run(app, host="127.0.0.1", port=8000)
