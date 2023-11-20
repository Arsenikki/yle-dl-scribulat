# Introduction
Scripts to scrape Yle Areena metadata with Playwright, and handle batch downloading using yle-dl tool. 

## Requirements
- Docker
- Python
- Playwright

## Usage
There's 3 different scripts. Each one described below

### Scrape series urls:
This script scrapes Yle Areena for episode urls as they are unpredictable.

1. Edit `seriesUrl` in `./tests/yle_areena_scrape.spec.js`
2. Scrape urls with playwright:
    ```
    npx playwright test
    ```
3. Episode urls in `./urls.txt`
4. If failed, following can be used to see what happens inside headed chromium
    ```
    npx playwright test -ui
    ```

### Bulk download series episodes
This script uses the `urls.txt` file to download each episode of a series. One download container is created per episode. 

**NOTE: Currently just hardcoded to wait 10s before launching next one to not overwhelm the host machine, but might need tweaking based on resources available!**

1. Run script
    ```bash
    python3 yle-dl-bulk-download.py
    ```
2. Output produced in `./downloads`

### Bulk download series episodes
This script renames episodes from `./downloads` directory. By default, dry run mode is used. Set `dry_run = False` to apply changes!

Before:
```
Itse Valtiaat : Paavon viimeiset kiusaukset: S12E194-2021-02-01T00:01.mkv 
```

After:
```
Itse.Valtiaat.S12E08.Paavon.viimeiset.kiusaukset.mkv
```
