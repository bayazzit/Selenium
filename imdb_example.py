from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("start-maximized");

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.imdb.com/")
driver.implicitly_wait(2)

def checkForBrokenImages():
    # Get the page for all images
    driver.find_elements(By.XPATH, "//*[@id='iconContext-chevron-right-inline']")[1].click()

    # Check for images
    img_list = driver.find_elements(By.TAG_NAME, 'img')
    for image in img_list:
        img_src = image.get_attribute('src')
        assert img_src[-3::] == 'jpg'

def getInfoCircus():
    # Save director, writer and stars to compare later
    director = driver.find_elements(By.CSS_SELECTOR, "a[href='/name/nm0000122/?ref_=tt_ov_dr']")[0].text
    writer = driver.find_elements(By.CSS_SELECTOR, "a[href='/name/nm0000122/?ref_=tt_ov_wr']")[0].text
    stars = driver.find_element(By.XPATH,
                                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul").text
    return director, writer, stars

def getInfoJazz():
    # Save director, writer and stars to compare later
    director = driver.find_elements(By.CSS_SELECTOR, "a[href='/name/nm0189076/?ref_=tt_ov_dr']")[0].text
    writer = driver.find_element(By.XPATH, "//body/div[@id='__next']/main[1]/div[1]/section[1]/section[1]/div[3]/section[1]/section[1]/div[3]/div[2]/div[1]/div[3]/ul[1]/li[2]/div[1]/ul[1]").text
    stars = driver.find_element(By.XPATH,
                                "//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul").text
    return director, writer, stars

def searchMovieShort(movie_name):
    driver.find_element(By.CSS_SELECTOR, '#home_img_holder').click()
    driver.find_element(By.CSS_SELECTOR, '#suggestion-search').send_keys(movie_name)
    driver.find_elements(By.CSS_SELECTOR, '.searchResult__constTitle')[0].click()

# Beginning of The Circus
# Get The Circus with long method
driver.find_element(By.CSS_SELECTOR, 'label#imdbHeader-navDrawerOpen--desktop .ipc-button__text').click()
WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Oscars')]")))
driver.find_element(By.XPATH, "//span[contains(text(),'Oscars')]").click()
driver.find_element(By.XPATH, "//a[contains(text(),'1929')]").click()
driver.find_elements(By.CSS_SELECTOR, "a[href='/title/tt0018773/?ref_=ev_nom']")[1].click()

c_first_director, c_first_writer, c_first_stars = getInfoCircus()

# Get The Circus with short method
searchMovieShort('The Circus')

c_second_director, c_second_writer, c_second_stars = getInfoCircus()

assert c_first_director == c_second_director
assert c_first_writer == c_second_writer
assert c_first_stars == c_second_stars

checkForBrokenImages()
# End of The Circus

# Beginning of The Jazz Singer
# Get The Jazz Singer with long method
driver.find_element(By.CSS_SELECTOR, '#home_img_holder').click()
driver.find_element(By.CSS_SELECTOR, 'label#imdbHeader-navDrawerOpen--desktop .ipc-button__text').click()
WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Oscars')]")))
driver.find_element(By.XPATH, "//span[contains(text(),'Oscars')]").click()
driver.find_element(By.XPATH, "//a[contains(text(),'1929')]").click()
driver.find_elements(By.CSS_SELECTOR, "div[class='event-widgets__award-category'] a[href='/title/tt0018037/?ref_=ev_nom'] ")[1].click()

j_first_director, j_first_writer, j_first_stars = getInfoJazz()

# Get The Jazz Singer with short method
searchMovieShort('The Jazz Singer')

j_second_director, j_second_writer, j_second_stars = getInfoJazz()

assert j_first_director == j_second_director
assert j_first_writer == j_second_writer
assert j_first_stars == j_second_stars

checkForBrokenImages()
# End of Jazz

driver.close()

print('Code applied successfully..')