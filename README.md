# pg essay scraper

downloads all paul graham essays into a csv. includes word counts and full text.

## requirements
- beautifulsoup4
- html2text
- pandas
- regex
- requests

## usage
```python
python script.py
```

outputs `essays.csv` in the current directory with:
- title
- word_counts
- texts

## notes
- handles both utf-8 and latin-1 encodings
- skips images and tables
- normalizes weird https urls
- will OVERWRITE existing essays.csv without warning

## limitations
afaict this is fragile af and will break if pg changes his site layout bc it relies on specific html structure. also no rate limiting rn so maybe don't hammer his server too hard

## disclaimer
idk about the legality of scraping pg's essays en masse, use at your own risk fam
