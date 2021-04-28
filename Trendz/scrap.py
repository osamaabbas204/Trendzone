import requests
from bs4 import BeautifulSoup


def scrapmobilelist(brand_name):

    
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f"https://propakistani.pk/price/brand/{brand_name}/") .text
    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all("div", class_="thumb-area")
    image_list = []
    title_list = []
    price_list = []
    tag_list = []
    for result in results:
        image = result.find("div", class_="thumb").a.img['data-lazy-src']
        title = result.find("div", class_="title").text
        price = result.find("div", class_="price").span.text
        strip_title = title.strip()
        tags = strip_title.replace(" ", "-")
        tag_list.append(tags.lower())
        image_list.append(image.strip())
        title_list.append(strip_title)
        price_list.append(price.strip())
    context = zip(image_list, title_list, price_list, tag_list)

    return context


def scrapmobiledetail(device_name):

    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f"https://propakistani.pk/price/{device_name}/") .text
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    data_list = []
    spec_list = []
    specs_list = []
    title = soup.find("h1", class_="title").strong.text
    price = soup.find("div", class_="price").span.text
    image = soup.find("div", class_="slickSlider").img['data-lazy-src']
    specs = soup.find("div", id="specifications")
    spec_list = specs.find_all("span")
    for spec in spec_list:
        specs_list.append(spec.text)
    datas = soup.find_all('div', class_="table-responsive")
    for data in datas:
        table_data = data.find_all("td")
        for num in table_data:
            data_list.append(num.text)
    detail = {"title": title, "price": price, "image": image,
              "data_list": data_list, "specs_list": specs_list}

    return detail
