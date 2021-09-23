import Config           # Own module imports
from Utils import *

from time import time       # Other imports
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import csv

print('\n')
post_url1=input("Enter the post url: ")
post_url = check_post_url(post_url1)


##### Writer csv
writer = csv.writer(open(Config.file_name, 'w', encoding='utf-8'))
# writer.writerow(['Name','Profile Heading','Email','Comment','Time'])

linkedin_username, linkedin_password = login_details()

start = time()       # Starting time
print('Initiating the process....')
##### Selenium Chrome Driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com')

username = driver.find_element_by_name(Config.username_name)
username.send_keys(linkedin_username)
sleep(0.5)

password = driver.find_element_by_name(Config.password_name)
password.send_keys(linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(30)

driver.get(post_url)
sleep(10)

# dropdown_button = driver.find_element_by_class_name(Config.dropdown_class)
# select=Select(dropdown_button)
# select.select_by_visible_text("Most recent")

print('Loading comments :', end=' ', flush=True)
load_more_comments(Config.load_comments_class, driver)

#comments = driver.find_elements_by_xpath('//span[@class="ember-view"]')
# this is bad because in case of comments with mentions or tags, it doesnt work
comments = driver.find_elements_by_class_name(Config.comment_class)
comments = [comment.text.strip() for comment in comments]

headlines = driver.find_elements_by_class_name(Config.headline_class)
headlines = [headline.text.strip() for headline in headlines]

emails = extract_emails(comments)

names = driver.find_elements_by_class_name(Config.name_class)
names = [name.text.split('\n')[0] for name in names]

times = driver.find_elements_by_class_name(Config.time_class)
times = [times.text.split('\n')[0] for times in times]

# print(type(comments))
# print(names)
# print(type(times[0]))
# print(times)

times_final=[]

for i in times:
    times_final.append(extract_time(i))

# print(times_final)



# print(comments[:10])
# print(names[:10])
# print(emails[:10])

write_data2csv(names, headlines, emails, comments,times_final, writer)
# csvData = pd.read_csv('comments_data.csv')
# csvData=csvData.dropna()
# print(csvData)


csvData=pd.read_csv('comments_data.csv',header=None, delim_whitespace=True)
csvData=csvData.dropna()
csvData.sort_values(["Time"],
                    axis=0,
                    ascending=[True],
                    inplace=True)
csvData.to_csv('comments_data.csv',index=False)
    


end = time()       # Finishing Time
time_spent = end-start # Time taken by script

print('Linkedin post comments scraped in: %.2f minutes (%d seconds)' % (((time_spent)/60),(time_spent)))

driver.quit()
