import scrapy


class ReviewSpider(scrapy.Spider):
    def __init__(self, book_title: str, *args, **kwargs):
        self.book_title = book_title
        super().__init__(*args, **kwargs)

    name = "rev_spider"

    def start_requests(self):
        start_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&query={self.book_title.replace(' ', '+')}"
        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        book_rel_url = response.css('td a::attr(href)').get()
        book_abs_url = response.urljoin(book_rel_url)
        yield scrapy.Request(book_abs_url, callback=self.review_parse)

    def review_parse(self, response):
        bt_text = response.css('h1::attr(aria-label)').get()
        book_title = bt_text.split(':')[1][1:]
        author = response.css('a span::text').getall()[1]

        review_elements = response.css('section.ReviewText__content span')
        reviews_list = []
        for review in review_elements:
            review_text = ''.join(review.xpath('.//text()').getall())
            reviews_list.append(review_text)

        yield {
            'book_tile': book_title,
            'author': author,
            'reviews': reviews_list
        }