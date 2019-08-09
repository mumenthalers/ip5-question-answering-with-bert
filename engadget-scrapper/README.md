# engadget-scrapper
Web Crawler for scrapping engadget articles

# Prerequisites

Make sure you have [pyenv](https://github.com/pyenv/pyenv) and [pipenv](https://github.com/pypa/pipenv)
installed.

# Usage

Execute `bin/scrap -s` to start scrapping the engadget news articles.
The output will be stored in `output/engadget-articles.json` by default.

But you can change the output by passing it to the command with `bin/scrap -s output/articles.json`
for example.
