# Realtor.ca Scraper

Lightweight Selenium-based scraper using `undetected-chromedriver`.

Requirements
- Python 3.8+
- Chrome / Chromium installed
- Python deps:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Chromedriver
- You need a ChromeDriver that matches your installed Chrome.
- Official download and instructions: https://sites.google.com/chromium.org/driver/
- On Linux you can also install via your package manager or download the matching release and place the `chromedriver` binary on your PATH.

Usage
Run the main script and set `city` and `max_pages` in `realtorca.py`, or modify the call in `main()`.

Example (simple):

```bash
python3 realtorca.py
```

What it does
- Automates the homepage search, selects the first autocomplete result, waits for results, and parses listing cards (`div.smallListingCard`) to extract Address, Price, Bedrooms, Bathrooms, SquareFootage, MLS and Link.

Notes
- This repository currently does not implement filtering by price, beds, or baths. Remove those flags from your commands.

License: MIT
