# wikisurf
Toy Scrapy project for crawling wikipedia.  Built to play "six degrees of separation" with wiki articles.

To use, set up a conda environment using environment.yml, run the "run_sixdgrees.sh" shell script, and provide a start and a target https://en.wikipedia.org.wiki/ URL (either the whole path or just relative to that path).

This is the initial working prototype and there are many improvements that should be made, such as:
- Using the wiki-provided "pages that link to this" tool to do a pseudo-bidirectional BFS to greatly reduce time + space usage.
- If given an invalid site, it should search for the closest valid URL and prompt if the user would like to use those
- Dealing with unicode, and/or other languages
- Storing the network maps that we scrape in a database cache instead of actually crawling every time.

Right now it does work, unless the start and end are too far apart such that we run out of memory for our network tree.  A couple of the mentioned improvements would fix that issue.

