import scrapy


class ZellburySpider(scrapy.Spider):
    name = "zellbury"
    allowed_domains = ["zellbury.com"]
    start_urls = ["https://zellbury.com/collections/men-basic-t-shirt"]

    def parse(self, response):
        category_link = response.css("a.menu-drawer__menu-item::attr(href)").getall()
        for link in category_link:
            full_link = response.urljoin(link)
            yield scrapy.Request(
                url=full_link,
                callback=self.parse_category,
            )

    def parse_category(self, response):
        product_links = response.css("a[href*='/products/']::attr(href)").getall()
        for link in product_links:
            full_link = response.urljoin(link)
            yield scrapy.Request(
                url=full_link,
                callback=self.parse_product,
            )

        next_page = response.css("a.action.next::attr(href)").get()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_category,
            )

    def parse_product(self, response):
        yield {
            "Title": response.css("div.product_title h1::text").get(),
            "Price": response.css("span.price-item::text").get().strip(),
            "Product-SKU": response.css("span.product-sku::text").get(),
            "Product-Barcode": response.css("span.product-barcode::text").get(),
            "Colors": response.css("input[name=Color]::attr(value)").getall(),
            "Sizes": response.css("input[name=Size]::attr(value)").getall(),
            "URL": response.url

        }
