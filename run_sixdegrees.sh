echo Enter start page:
read startpage
echo Enter end_page:
read endpage
scrapy crawl six_degrees -a start_url=$startpage -a target=$endpage
