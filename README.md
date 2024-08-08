## Crawl data

By default it'll look for feeds.txt in the currrent directory
```bash
python download_content.py 
```
or 

```bash
python download_content.py --feed-path feeds.txt
```
You can add your desired feeds to the feeds.txt

## Launch app

By default it'll look for feeds.db in the currrent directory

```bash
python app.py
```
or

```bash
python -m app.app --data-path feeds.db
```
