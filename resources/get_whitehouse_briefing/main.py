from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


outfileName = "url_list.txt"
outfile = open(outfileName, "w")

url = "https://www.whitehouse.gov/briefing-room/page/"

opt = webdriver.ChromeOptions()
#opt.add_argument("headless")
opt.add_argument("window-size=1920x1080")
#opt.add_argument("disable-gpu")
opt.add_argument("log-level=3")

driver = webdriver.Chrome("chromedriver", chrome_options=opt)

for j in range(310):
    idx = 1 + j
    print(str(idx) + "th page\n")
    driver.get("https://www.whitehouse.gov/briefing-room/page/" + str(idx))
    time.sleep(2)

    linkboxes = driver.find_elements(By.CLASS_NAME, "news-item__title")

    for el in linkboxes:
        url = el.get_attribute("href")
        outfile.write(url + "\n")

outfile.close()

targets = open(outfileName)
txt = open("whitehouse briefing.txt", "w")

for line in targets:
    print(line)
    url = line.strip()
    try:
        driver.get(url)
        time.sleep(1)
        section = driver.find_element(By.CLASS_NAME, "body-content")
        txt.write(section.text)
        time.sleep(1)
    except:
        print("error occured")
        time.sleep(1)
        continue

txt.close()
targets.close()

