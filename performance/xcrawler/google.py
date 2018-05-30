from xcrawler import XCrawler, Page, PageScraper


class UrlsScraper(PageScraper):
    def visit(self, page):
        return [Page('https://google.com', QuestionScraper())]


class QuestionScraper(PageScraper):
    def extract(self, page):
        return page.css_text('input')[0]


start_pages = [ Page("https://google.com", UrlsScraper()) ]
crawler = XCrawler(start_pages)
crawler.config.output_file_name = "google.csv"
crawler.config.number_of_threads = 1
crawler.run()
