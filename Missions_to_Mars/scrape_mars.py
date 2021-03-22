from splinter import Browser
from bs4 import BeautifulSoup


mars_scrap = {}
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\Program Files\Google\Chrome\Application\chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # create surf_data dict that we can insert into mongo
    mars_news = {}
    url = 'https://mars.nasa.gov/news/'
    html = browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    data_containers = soup.find('div', class_='list_text')
    # print(len(data_containers))
    # data_containers
    # latest News Title Text.
    news_ = data_containers.find(class_='content_title')
    news_title = news_.string
    # latest News Paragraph
    tit_body = data_containers.find(class_='article_teaser_body')
    news_p = tit_body.string
    mars_news
    mars_scrap['news_title'] = news_title
    mars_scrap['news_p'] = news_p
    browser.quit()
    return mars_scrap


def Mars_Space_Images(): 
    browser = init_browser()
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')
    header = soup1.find('div', class_='header')
    img_ = header.find(class_='floating_text_area')
    link_img = img_.find('a', class_='showimg fancybox-thumbs')
    href_img = link_img['href']
    # split_url = href_img.split('/')
    # image_name = split_url[-1] # image name
    # local_path_image = '../Images/' + image_name
    # title = link_img.text
    featured_image_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + href_img
    #response = requests.get(featured_image_url, stream=True)
    #with open(local_path_image, 'wb') as out_file:
    #shutil.copyfileobj(response.raw, out_file)
    mars_scrap['featured_image_url'] = featured_image_url
    browser.quit()
    return mars_web

def Mars_Facts():
    browser = init_browser()
    URL='https://space-facts.com/mars/'
    tables = pd.read_html(URL) # tablepress-p-mars
    # tables
    marts = tables[0]
    marts_facts = marts.rename(columns={0: "Facts", 1: "Value"})
    # marts_facts.to_html('Mars_Facts.html', index=False, border=1)
    marts_fact = marts_facts.to_html()
    #print(marts_fact);
    mars_news['marts_facts'] = marts_fact
    browser.quit()
    return mars_news

def Mars_Hemispheres():
    browser = init_browser()      
    USGS_URL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_URL)
    html_USGS = browser.html
    soup2 = BeautifulSoup(html_USGS, 'html.parser')
    div_img = soup2.find_all('div', class_='description')
    src_imgs=[]
    # img_mars_name = []
    title=[]
    for result in div_img:
        name = result.find('a', attrs={'class':'itemLink product-item'})['href']
        src_imgs.append('https://astrogeology.usgs.gov/' + name)
        title_mars= result.find('h3').text
        title.append(title_mars)
        # title
    img_url=[]
    for imgsrc in src_imgs:
        browser.visit(imgsrc)
        img_USGS = browser.html
        soup3 = BeautifulSoup(img_USGS, 'html.parser')
        results = soup3.find('li')
        href_full_img = results.find('a')['href']
        img_url.append(href_full_img)
    #     print(href)
        # img_url
        hemisphere_image_urls=[]
        title_ = ["title"]
        urlimg_ = ["url_img"]

    for i in range(len(title)):
        hemisphere_image_urls.append(dict.fromkeys(title_,title[i]))

    for l in range(len(img_url)):
        hemisphere_image_urls[l].update(dict.fromkeys(urlimg_,img_url[l]))
        # hemisphere_image_urls

    mars_news['hemisphere_image_urls'] = hemisphere_image_urls
    browser.quit()
    return mars_news
