import random
import requests
from bs4 import BeautifulSoup
from .models import Laptop, Specification, Mobile, Mobilespec
# import json
# import pandas as pd
# import re


def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                 "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
                 ]

    return random.choice(uastrings)


def parse_url(url):

    headers = {'User-Agent': GET_UA()}
    content = None
    try:
        response = requests.get(url, headers=headers)
        ct = response.headers['Content-Type'].lower().strip()

        if 'text/html' in ct:
            content = response.content
            soup = BeautifulSoup(content, "lxml")
        else:
            content = response.content
            soup = None

    except Exception as e:
        print('Error', str(e))

    return content, soup, ct


def scrapmobile():

    mobilelist = ['samsung_mobiles_prices', 'apple', 'vivo', 'xiaomi', 'oppo',
                  'huawei', 'google', 'oneplus', 'nokia', 'asus', 'infinix', 'realme']

    for mobile in mobilelist:
        scrapmobileviapages(mobile)
    pass


def scraplaptop():

    laptoplistmega = ['apple', 'hp', 'dell',
                      'microsoft', 'asus', 'lenovo', 'acer', 'msi']

    laptoplistpak = ['hp-laptops', 'dell', 'microsoft',
                     'asus-laptops', 'lenovo-laptops', 'acer', 'msi-gaming-laptops']

    for laptop in laptoplistmega:
        scraplaptopmega(laptop)

    for laptop in laptoplistpak:
        scraplaptopPaklap(laptop)
    pass


def popularMobile():
    test = parse_url(
        f"https://propakistani.pk/price/popular-phones-price-in-pakistan/")
    soup = test[1]
    popularMobiles = soup.find_all('div', class_='title')
    popularlist = []
    for mobile in popularMobiles:
        popularlist.append(mobile.text.replace("\n", ""))
    print(popularlist)

    for popular in popularlist:
        if Mobile.objects.filter(title=popular):
            Mobile.objects.filter(title=popular).update(status="popular")

    pass


def latestMobile():
    test = parse_url("https://priceoye.pk/store")
    soup = test[1]
    latestMobiles = soup.find_all('h4', class_='p3')
    latestlist = []
    for mobile in latestMobiles:
        mobile1 = mobile.text.replace("\n", "")
        latestlist.append(mobile1.strip())
    print(latestlist)

    for latest in latestlist:
        if Mobile.objects.filter(title=latest):
            Mobile.objects.filter(title=latest).update(status="latest")
            print("Latest mobile updated ", latest)

    pass


def popularLaptop():
    popularlist = []
    # popular macbook from paklap.pk
    test2 = parse_url(
        "https://www.paklap.pk/apple-products/apple-macbooks.html")
    soup = test2[1]
    container = soup.find('ol', class_='products list items product-items')
    productInfo = container.find_all('div', class_='product-item-info')
    productInfo.pop(-1)
    for product in productInfo:
        title = product.find(
            'strong', class_='product name product-item-name').a.text
        popularlist.append(title.strip())
    # popular laptop from paklap.pk
    test3 = parse_url(
        "https://www.paklap.pk/laptops-prices.html")
    soup = test3[1]
    container = soup.find('ol', class_='products list items product-items')
    productInfo = container.find_all('div', class_='product-item-info')
    productInfo.pop(-1)
    for product in productInfo:
        title = product.find(
            'strong', class_='product name product-item-name').a.text
        popularlist.append(title.strip())

    test = parse_url(
        f"https://www.mega.pk/")
    test1 = parse_url(
        f"https://www.mega.pk/ajax.php?key=home-grid&option1=7&option2=34")
    soup = test[1]
    soup1 = test1[1]
    laptopdiv = soup.find('div', id='mycarousel1')
    laptopdiv1 = soup1.find('div', id='mycarousel34')
    names1 = laptopdiv1.find_all('div', id='lap_name_div')
    Names = laptopdiv.find_all('div', id='lap_name_div')
    for name in Names:
        popularlist.append(name.text.replace("\n", ""))
    for laptop in names1:
        popularlist.append(laptop.text.replace("\n", ""))
    print(popularlist)
    for popular in popularlist:
        if Laptop.objects.filter(title=popular):
            Laptop.objects.filter(title=popular).update(status="popular")
        else:
            print("----------------------- This ", popular, " Not Available")

    pass


def scrapmobileviapages(brand_name):

    html_data = parse_url(f"https://propakistani.pk/price/brand/{brand_name}/")
    soup = html_data[1]
    pagelink = soup.find_all('a', class_="page-link")
    if 'samsung_mobiles_prices' in brand_name:
        scrapmobilelist(brand_name)
    elif pagelink:
        pages = pagelink[-2].text
        num = int(pages)
        i = 1
        while i <= num:
            tag = f'{brand_name}/page/{i}'
            scrapmobilelist(tag)
            i += 1
    else:
        scrapmobilelist(brand_name)

    return None


def scrapmobilelist(brand_name):
    brand1 = brand_name.split('/')
    brand2 = brand1[0]
    print(brand2)
    html_data = parse_url(f"https://propakistani.pk/price/brand/{brand_name}/")
    soup = html_data[1]
    results = soup.find_all("div", class_="thumb-area")
    image_list = []
    title_list = []
    price_list = []
    tag_list = []
    status_list = []
    for result in results:
        try:
            image = result.find("div", class_="thumb").a.img['data-lazy-src']
        except:
            image = "error"
        title = result.find("div", class_="title").text
        href = result.find("div", class_="title").a['href']
        price = result.find("div", class_="price").span.text
        status = result.find('div', class_='score mt-0 mb-2')
        if status:
            status1 = status.text
        else:
            status1 = 'None'
        strip_title = title.strip()
        tags = href.split('/')
        status_list.append(status1)
        tag_list.append(tags[4])
        image_list.append(image.strip())
        title_list.append(strip_title)
        price_list.append(price.strip())
    context = zip(image_list, title_list, price_list, tag_list, status_list)

    # For saving Data in Database(Mobile) table
    Query = Mobile.objects.all().filter(brand=brand2)
    for img, title, price, tag, status in context:
        title_cn = False
        img_cn = False
        price_cn = False
        tag_cn = False
        status_cn = False
        for obj in Query:
            if obj.title == title:
                title_cn = True
                if obj.image == img:
                    img_cn = True
                if obj.price == price:
                    price_cn = True
                if obj.tag == tag:
                    tag_cn = True
                if obj.status == status:
                    status_cn = True
        if not title_cn:
            reg = Mobile(title=title, price=price, image=img,
                         tag=tag, status=status, brand=brand2)
            reg.save()
        elif title_cn:
            if not img_cn:
                Mobile.objects.filter(title=title).update(image=img)
            if not price_cn:
                Mobile.objects.filter(title=title).update(price=price)
            if not tag_cn:
                Mobile.objects.filter(title=title).update(tag=tag)
            if not status_cn:
                Mobile.objects.filter(title=title).update(status=status)

    return context


def scrapmobiledetail(device_name):

    html_data = parse_url(f"https://propakistani.pk/price/{device_name}/")
    soup = html_data[1]
    keyList = ["Price in Pakistan", "Technology", "2GBands", "3GBands", "4GBands", "5GBands", "Speed", "GPRS", "EDGE", "Announced", "Status",
               "Dimensions", "Weight", "Build", "Sim", "Type", "Size", "Resolution", "Multitouch", "Protection", "OS", "Chipset", "CPU", "GPU", "Cardslot",
               "Internal", "Others", "Primary", "Features", "Video", "Secondary", "Others", "Alerttypes", "Loudspeaker", "3.5mmjack", "WLAN", "Bluetooth",
               "GPS", "NFC", "Infraredport", "Radio", "USB", "Sensors", "Messaging", "Browser", "Java", "Type", "Charging10W", "SARUS", "Colors"]
    data_list = {key: '-' for key in keyList}
    keyList = ["camera", "processor", "internal_storage",
               "battery", "ram", "display", "color"]
    Dict_spec = {key: None for key in keyList}
    title = soup.find("h1", class_="title").strong.text
    # darazdata = darazmobileprice(title)
    price = soup.find("div", class_="price").span.text
    image = soup.find("div", class_="slickSlider").img['data-lazy-src']
    specs = soup.find_all("div", class_="row spec-wr mx-0")
    rating = soup.find("div", class_="review-head").div.div.span.text
    rating1 = int(rating)
    print(rating)
    status = soup.find('div', class_='score mt-0 mb-2').text
    for spec in specs:
        tex0 = spec.find('span').text
        tex = spec.find('div', class_='col spec-dt').text
        if 'Camera' in tex:
            Dict_spec['camera'] = tex0
        elif 'Processor' in tex:
            Dict_spec['processor'] = tex0
        elif 'Internal Storage' in tex:
            Dict_spec['internal_storage'] = tex0
        elif 'Battery' in tex:
            Dict_spec['battery'] = tex0
        elif 'Memory' in tex:
            Dict_spec['ram'] = tex0
        elif 'Display' in tex:
            Dict_spec['display'] = tex0
    datas = soup.find_all('div', class_="table-responsive")
    for data in datas:
        table_data = data.find_all("tr")
        for dat in table_data:
            child = dat.findChildren()
            if child:
                key = child[0].text.replace(" ", "")
                if key in data_list.keys():
                    data_list[key] = child[1].text

    detail = {"title": title, "price": price, "image": image,
              "data_list": data_list, "specs_list": Dict_spec, 'status': status, "rating": int(rating)}

    Query = Mobilespec.objects.filter(title=title)
    obj1 = None
    for obj in Query:
        obj1 = obj
        tag_b = obj.tag == device_name
        camera_b = obj.camera == Dict_spec['camera']
        processor_b = obj.processor == Dict_spec['processor']
        internal_b = obj.internal_storage == Dict_spec['internal_storage']
        battery_b = obj.battery == Dict_spec['battery']
        ram_b = obj.ram == Dict_spec['ram']
        display_b = obj.display == Dict_spec['display']
    if Query:
        if not tag_b:
            Mobilespec.objects.filter(title=title).update(tag=device_name)
        if not camera_b:
            Mobilespec.objects.filter(title=title).update(
                camera=Dict_spec['camera'])
        if not processor_b:
            Mobilespec.objects.filter(title=title).update(
                processor=Dict_spec['processor'])
        if not internal_b:
            Mobilespec.objects.filter(title=title).update(
                internal_storage=Dict_spec['internal_storage'])
        if not battery_b:
            Mobilespec.objects.filter(title=title).update(
                battery=Dict_spec['battery'])
        if not ram_b:
            Mobilespec.objects.filter(title=title).update(ram=Dict_spec['ram'])
        if not display_b:
            Mobilespec.objects.filter(title=title).update(
                display=Dict_spec['display'])
    else:
        reg = Mobilespec(mobile=Mobile.objects.get(title=title),
                         title=title,
                         tag=device_name,
                         rating=rating1,
                         camera=Dict_spec['camera'],
                         processor=Dict_spec['processor'],
                         internal_storage=Dict_spec['internal_storage'],
                         battery=Dict_spec['battery'],
                         ram=Dict_spec['ram'],
                         display=Dict_spec['display'],
                         color=Dict_spec['color'])
        reg.save()

    return detail


# def darazmobileprice(title):
#     title1 = title.replace(" ", "+")
#     print(title1)
#     html_data = parse_url(
#         f"https://www.daraz.pk/catalog/?q={title1}&_keyori=ss&from=input&spm=a2a0e.home.search.go.166c4937sDoNHy")
#     soup = html_data[1]
#     for script in soup.select('script'):
#         print(script.text)
#         print("===================================================================================================================")
#         if 'window.pageData=' in script:
#             script = script.text.replace('window.pageData=', '')
#             print(script)
#             break
#     items = json.loads(script)
#     print(items)
#     # results = []

#     # for item in items:
#     #     # print(item)
#     #     # extract other info you want
#     #     row = [item['name'], item['priceShow'],
#     #            item['productUrl'], item['ratingScore']]
#     #     results.append(row)

#     # df = pd.DataFrame(results, columns=[
#     #                   'Name', 'Price', 'ProductUrl', 'Rating'])

#     # print(df.head())
#     pass


def scraplaptopshophive(brand_name):
    title_list = []
    img_list = []
    price_list = []
    tag_list = []
    test = parse_url(
        f"https://www.shophive.com/laptops-computers/laptops/{brand_name}?product_list_limit=25")
    soup = test[1]
    laptops = soup.find_all(
        'li', class_='item product product-item product-item-toki')
    for laptop in laptops:
        title = laptop.find('h3', class_='product-name').a.text
        image = laptop.find(
            'div', class_='product-photo').a.span.span.img['data-original']
        prices = laptop.find('span', class_='price')
        if prices:
            price = prices.text
        else:
            price = 'No Data'
        strip_title = title.strip()
        tags = strip_title.replace(" ", "-")
        tag_list.append(tags.lower())
        title_list.append(title)
        img_list.append(image)
        price_list.append(price)
    print(price_list)
    context = zip(img_list, title_list, price_list, tag_list)
    return context


def scraplaptopmega(brand_name):
    print(brand_name)
    print("..........................................................................................................................................")
    test = parse_url(f"https://www.mega.pk/laptop-{brand_name}/")
    soup = test[1]
    laptops = soup.find_all('div', class_='lap_thu_box bg-color-white')
    for laptop in laptops:
        link = laptop.find('div', class_='wrapper1').a['href']
        title = laptop.find('div', id='lap_name_div').h3.a.text
        image = laptop.find('div', class_='wrapper1').a.img['data-original']
        price = laptop.find('div', class_='cat_price').text
        links = link.split('/', 4)
        tags2 = links[-1].split('.')
        tag2 = tags2[0]
        finaltag = tag2.replace('/', '-')
        finalprice = price.strip()

        if Laptop.objects.filter(title=title):
            laptop = Laptop.objects.get(tag1=finaltag)
            if not laptop.image == image:
                print('Image Update for ', title)
                Laptop.objects.filter(title=title).update(image=image)
            if not laptop.price == finalprice:
                Laptop.objects.filter(title=title).update(price=finalprice)
                print('price Update for ', title)
            if not laptop.tag1 == finaltag:
                Laptop.objects.filter(title=title).update(tag1=finaltag)
                print('tag Update for ', title)
            if not laptop.link == link:
                Laptop.objects.filter(title=title).update(link=link)
                print('link Update for ', link)
        else:
            reg = Laptop(title=title, price=finalprice, image=image,
                         tag1=finaltag, site='Mega', brand=brand_name)
            reg.save()
            print('New object added to Database', title)

    pass


def scraplaptopdetailmega(device_name):
    device = device_name.replace('-', '/', 1)
    datadict = {}
    test = parse_url(f"https://www.mega.pk/laptop_products/{device}.html")
    soup = test[1]
    image = soup.find('div', itemprop='image').img['data-original']
    title = soup.find('h1', class_='product-title').span.text
    datas2 = soup.find_all('td', class_='val')
    datas1 = soup.find_all('td', class_='ha')
    datas = zip(datas1, datas2)
    for data1, data2 in datas:
        data3 = data1.text.replace(" ", "")
        data4 = data3.replace('\xa0', '').strip()
        dataspec = data2.text
        if dataspec == '\xa0':
            dataspec = ''
        datadict.update({data4: dataspec.strip()})
    detail = {"datadictmega": datadict.items(), "datadict": datadict,
              "imageMega": image}

    # For saving Data in Database(Specification) table

    if not Specification.objects.filter(title=title):
        reg = Specification(
            laptop=Laptop.objects.get(title=title),
            tag=device_name,
            title=title,
            generation=datadict['ProcessorType'],
            processor=datadict['ProcessorType'],
            processor_speed=datadict['ProcessorSpeed'],
            installed_ram=datadict['InstalledRAM'],
            type_ofmemory=datadict['Typeofmemory'],
            hard_drivesize=datadict['Harddrivesize'],
            hard_drivespeed=datadict['Harddrivespeed'],
            optical_drive=datadict['OpticalDrive'],
            ssd=datadict['SSD'],
            type_ofharddrive=datadict['Typeofharddrive'],
            dedicated_graphics=datadict['Dedicatedgraphics'],
            graphics_processor=datadict['Graphicsprocessor'],
            backlight=datadict['Backlight'],
            screen_size=datadict['Screensize'],
            screen_surface=datadict['Screensurface'],
            screen_resolution=datadict['Screenresolution'],
            touchscreen=datadict['Touchscreen'],
            color=datadict['Colors'],
            fingerprint_reader=datadict['FingerprintReader'],
            numeric_keyboard=datadict['Numerickeyboard'],
            backlit_keyboard=datadict['Backlitkeyboard'],
            bluetooth=datadict['Bluetooth'],
            lan=datadict['LAN'],
            wireless_wifi=datadict['Wireless/Wifi'],
            wifi_type=datadict['Type'],
            condition='New', usb=datadict['USB'],
            hdmi=datadict['HDMI'],
            camera=datadict['Camera'],
            operating_system=datadict['Operatingsystem(Primary)'],
            manual=datadict['Manual'],
            product_page=datadict['Productpage'],
            warranty='1 Year Local Warranty')
        reg.save()
    # if titlep: ****************** update ************************************
    #    if not tagp:

    return detail


def scraplaptopPaklap(brand_name):
    print(brand_name)
    print("..........................................................................................................................................")
    if not "apple-macbooks" == brand_name:
        test = parse_url(
            f"https://www.paklap.pk/laptops-prices/{brand_name}.html")
    else:
        test = parse_url(
            "https://www.paklap.pk/apple-products/apple-macbooks.html")
    soup = test[1]
    container = soup.find('ol', class_='products list items product-items')
    productInfo = container.find_all('div', class_='product-item-info')
    productInfo.pop(-1)
    for product in productInfo:
        image = product.find('span', class_='product-image-wrapper').img['src']
        title = product.find(
            'strong', class_='product name product-item-name').a.text
        title1 = title.strip()
        href = product.find(
            'strong', class_='product name product-item-name').a['href']
        links = href.replace('https://www.paklap.pk/', '')
        tag = links.replace('.html', '')
        price = product.find('span', class_='price').text

        if brand_name == "asus-laptops":
            brand_name = "asus"
        elif brand_name == "hp-laptops":
            brand_name = "hp"
        elif brand_name == "lenovo-laptops":
            brand_name = "lenovo"
        elif brand_name == "msi-gaming-laptops":
            brand_name = "msi"
        elif brand_name == "apple-macbooks":
            brand_name = "apple"

        if Laptop.objects.filter(title=title1):
            laptop = Laptop.objects.get(title=title1)
            if not laptop.image == image:
                print('Image Update for ', title1)
                Laptop.objects.filter(title=title1).update(image=image)
            if not laptop.price == price:
                Laptop.objects.filter(title=title1).update(price=price)
                print('price Update for ', title1)
            if not laptop.tag1 == tag:
                Laptop.objects.filter(title=title1).update(tag1=tag)
                print('tag Update for ', title1)
            if not laptop.link == href:
                Laptop.objects.filter(title=title1).update(link=href)
                print('link Update for ', title1)
        else:
            reg = Laptop(title=title1, price=price, image=image,
                         tag1=tag, site='Paklap', brand=brand_name, link=href)
            reg.save()
            print('New object added to Database', title1)
    pass


def scrapdetailPaklap(device_name):
    datadict = {}
    test = parse_url(f"https://www.paklap.pk/{device_name}.html")
    soup = test[1]
    title = soup.find('span', class_='base').text
    im = soup.find('img', class_='fotorama__img magnify-opaque magnify-opaque')
    detaillabel = soup.find_all('th', class_='col label')
    detaildata = soup.find_all('td', class_='col data')
    detail = zip(detaillabel, detaildata)
    for label, data in detail:
        datadict.update({label.text.strip(): data.text.strip()})
    detail = {"datadictPaklap": datadict.items()}
    print(im)
    if not Specification.objects.filter(title=title):
        reg = Specification(
            laptop=Laptop.objects.get(tag1=device_name),
            tag=device_name,
            title=title,
            generation=datadict['Generation'],
            processor=datadict['Processor Type'],
            processor_speed=datadict['Processor Speed'],
            installed_ram=datadict['Installed RAM'],
            type_ofmemory=datadict['Type of memory'],
            hard_drivesize=datadict['Hard drive size'],
            hard_drivespeed=datadict['Hard drive speed'],
            optical_drive=datadict['Optical Drive'],
            type_ofopticaldrive=datadict['Type of optical drive'],
            ssd=datadict['SSD'],
            type_ofharddrive=datadict['Type of harddrive'],
            dedicated_graphics=datadict['Dedicated graphics'],
            graphics_memory=datadict['Graphics memory'],
            type_ofgraphics_memory_shared=datadict['Type of graphics memory'],
            switchable_graphics=datadict['Switchable graphics'],
            graphics_processor=datadict['Graphics processor'],
            backlight=datadict['Backlight'],
            screen_size=datadict['Screen size'],
            screen_surface=datadict['Screen surface'],
            screen_resolution=datadict['Screen resolution'],
            touchscreen=datadict['Touchscreen'],
            color=datadict['Color'],
            fingerprint_reader=datadict['Fingerprint Reader'],
            numeric_keyboard=datadict['Numeric keyboard'],
            backlit_keyboard=datadict['Backlit keyboard'],
            bluetooth=datadict['Bluetooth'],
            lan=datadict['LAN'],
            wireless_wifi=datadict['Wireless/Wifi'],
            wifi_type=datadict['Type'],
            condition=datadict['Condition'], usb=datadict['USB'],
            hdmi=datadict['HDMI'],
            camera=datadict['Camera'],
            operating_system=datadict['Operating system (Primary)'],
            manual=datadict['Manual'],
            product_page=datadict['Product page'],
            warranty=datadict['Warranty'])
        print("Laptop Detail is saved in the database...............................................................")
        reg.save()
    return detail


def priceoye(brand_name):
    brand1 = brand_name.strip().replace(" ",  "+")
    test = parse_url(f"https://priceoye.pk/search?q={brand1}")
    soup = test[1]
    product = soup.find("div", class_="productBox")
    link = product.find("a")["href"]
    title = product.find("h4", class_="p3").text
    price = product.find("div", class_="price-box").text
    print(price.strip())

    return {"price": price.strip().replace("\n", ""), "title": title.strip().replace("\n", ""), "link": link}


# def pricetelemart():
#     test = parse_url(
#         f"https://www.telemart.pk/search?query=samsung%20galaxy%20a52&refinementList%5Bcategories%5D%5B0%5D=Mobiles%20%26%20Tablets")
#     soup = test[1]
#     print
#     allProduct = soup.find_all('div', class_="col-sm-3 box")
#     print(allProduct)
#     for product in allProduct:
#         print(product)
#     pass


# popularMobile()
# popularLaptop()
