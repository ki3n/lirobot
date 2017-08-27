from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

##################################################################PARAMETERS#################################################################
#DO NOT RUN TWO INSTANCES OF THIS SCRIPT AT THE SAME TIME... IT WILL BE DETECTED
email = ""  #example@email.com
password = ""              #exact password
job_keyword = "Machine Learning"         #your search term on the linkedin.com/jobs page
location = "United States"             #the location you're looking for jobs with format: "City, State"

#put terms into the "unqualifiers" list to prevent a job posting from being added to your csv file.
#this is only done by searching for words in the title of the job post...
unqualifiers = ['lead', 'sr', 'sr.', 'senior', 'system', 'financial', 'director', 'manager', 'master']

#the amount of time needed to rest between some actions, usually for waiting for elements on linkedin.com to load
#increase if you're having trouble finding elements on the page
sleep_sec_interval = 5

#the page_down_num variable might have to be modified
#elements on the search results page returned by linkedin.com/jobs are loaded as you scroll down
#simply put, increase this number if you have to so that the script scrolls down the page until you can see the page numbering
#otherwise, the robot won't be able to scrape every link from the page
page_down_num = 10

#default is opened in 'a' mode which prevents truncating the csv file upon opening
csv_file_name = 'prospective.csv'
###############################################################################################################################



print "Opening web browser."
##################WEB BROWSER#########################
#startup/visiting page
driver = webdriver.Firefox() #YOU MUST MODIFY THIS IF YOU DO NOT WANT TO USE FIREFOX
driver.implicitly_wait(10)

print "Visiting LinkedIn.com."
driver.get("https://www.linkedin.com/")
assert "LinkedIn" in driver.title
######################################################



print "Logging in with script credentials."
#####################LOGIN############################
#email
email_elem = driver.find_element_by_id("login-email")
email_elem.clear()
email_elem.send_keys(email)

#password
pass_elem = driver.find_element_by_id("login-password")
pass_elem.clear()
pass_elem.send_keys(password)

#sign in button
login_button = driver.find_element_by_id("login-submit")
login_button.send_keys(Keys.RETURN)
assert "Please try again" not in driver.page_source
######################################################



print "Visiting the LinkedIn.com jobs page."
#################JOBS PAGE############################
sleep(sleep_sec_interval)
driver.get("https://www.linkedin.com/jobs/")
assert "Jobs" in driver.title
######################################################



print "Applying script search criteria."
#################JOBS PAGE SEARCH#####################
#Job title
keyword_search = driver.find_element_by_css_selector('input[placeholder="Search jobs by title, keyword or company"]')
keyword_search.clear()
keyword_search.send_keys(job_keyword)

#Location
location_search = driver.find_element_by_css_selector('input[placeholder="City, state, postal code or country"]')
location_search.clear()
location_search.send_keys(location)

#Search button
sleep(sleep_sec_interval)
location_search.send_keys(Keys.RETURN)
sleep(sleep_sec_interval)
assert "Showing 0 results" not in driver.page_source
######################################################



print "Scraping job posting links."
#############JOB POST SCRAPING LOOP###################
from bs4 import BeautifulSoup
import re

jobs = set() 
pattern = re.compile('/jobs/view/\S*')

#retrieving all posting links
while True:
    #scrolling page to load job posting links
    for x in range(0, page_down_num):
        sleep(0.5)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    sleep(sleep_sec_interval)

    #parsing the links
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    #scrapes all the job links on the pages, 
    #notice above: a set is used to remove duplicates and a pattern is used to ignore links that are not job postings
    for link in soup.find_all('a', href=True):
        if pattern.match(link['href']):
            job_posting_link = "https://www.linkedin.com%s" % link['href']
            jobs.add(job_posting_link)
    sleep(sleep_sec_interval)
    
    #flow of code controlled with exceptions... bad code, but it works well
    #clicks on the next page until an exception is thrown for not having a higher page button to click
    try:
        next_page = driver.find_element_by_css_selector('li.active + li button')
        next_page.click()
    except:
        break
assert len(jobs) > 0
print "%d job posting links scraped.\n" % len(jobs)
######################################################



###################JOB APPLICATION LOOP###############
#iterate through the set of links and writes the job title, description, and url to a .csv file
def write_job_to_csv(job_writer, soup, driver, job_title):
    
    #content will not load until the "See More" button is clicked
    see_more_button = driver.find_element_by_css_selector('button[class="view-more-icon"]')
    see_more_button.click()
    sleep(sleep_sec_interval)
    
    #job description
    job_description = soup.find("div", {"id": "job-details"})
    job_description = job_description.text.replace(',', '').replace('\n', '').encode('utf-8')

    #job link
    job_link = driver.current_url
    
    job_writer.writerow([job_title, job_description, job_link])

###############SCRAPING THE JOB POSTINGS#################
import csv
with open(csv_file_name, 'a') as csvfile:
    job_writer = csv.writer(csvfile, delimiter=',')

    while len(jobs) > 0:
        #visits the next job link
        driver.get(jobs.pop())
        
        #sleeps to wait elements load on page
        sleep(sleep_sec_interval)
        
        #gets the page source code and extracts the job title
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_title = soup.h1.text.replace(',', '').replace('\n', '').encode('utf-8').lower()
        
        #determines if any of the words in the job title appear in the unqualifiers list you provide
        #else, it writes description to to the .csv
        if(not any(x in job_title for x in unqualifiers)):
            write_job_to_csv(job_writer, soup, driver, job_title)
	
	#sleeps to decrease request frequency per time interval
	sleep(sleep_sec_interval)
    csvfile.close()
driver.close()
######################################################
















