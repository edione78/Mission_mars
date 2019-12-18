from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

def scrape_info():
    news = {}

    # Visit mars.nasa.gov/newa
    browser = Browser('chrome')
    browser.visit("https://mars.nasa.gov/news/")
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title
    news_title = soup.find('div', class_='content_title').a.text
    print(news_title)

    #Get the paragraph of news
    paragraph = soup.find('div', class_='article_teaser_body').text
    print(paragraph)

    # Store data in a dictionary
    news= {
        "Title": news_title,
        "Paragraph": paragraph,
        
    }

    #visit nasa site for image
    browser = Browser('chrome')
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)

    #get the full image
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()
    time.sleep(5)

    #scrape image into soup
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()
    time.sleep(5)

    #get url for image
    soup = bs(browser.html, 'html.parser')
    result=soup.find('figure',class_="lede")
    featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]
    featured_image_url

    #store image in news
    news['featured_image']=featured_image_url

    # Visit the Mars Weather twitter account 
    browser = Browser('chrome')
    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)

    # Find tweet title on mars weather 
    soup = bs(browser.html, 'html.parser')
    mars_weather = soup.find('div', class_="js-tweet-text-container")
    weather=mars_weather.p.text
    print(weather)

    #Save the tweet text for the weather report as a variable called `mars_weather`.
    # Store data in a dictionary
    news['mars_weather']=weather

    import pandas as pd
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    df

    #convert data into html
    data=df.to_html()
    data

    #store masrs facts
    news['facts']=data

    #open browser to scrape the mars hemisphere image
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #create the list of images
    hemisphere_image_urls = []
    
    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")
    
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        time.sleep(1)
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()
    
    print(hemisphere_image_urls)


    news['hemisphere']=hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()
    # Return results
    return news

if __name__ == "__main__":
    print(scrape_info())