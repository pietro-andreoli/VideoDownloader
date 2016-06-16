
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import Video
import os.path

# Request the name of the file
webpage_input = input("Enter Website: ")
#---website = get_episode_list_page(webpage_input).splitlines()
#---print(website)
#print(website)
# Open the file with reading permission
website = open('webpage.html', 'r', encoding='utf8')
episodes_to_download = input('Enter the episodes in the following format: \n1,2,6,8,100 etc \nor\n1-100,3')
download_list = []

def get_url(url_list, a_href_line):
    # String variable that holds the current URL
    url = ''
    # Boolean that states whether the first quote of the tag has been found. If false, then we have not found a quote, but if true then we have found the first quote
    first_quote_found = False
    # Variable that holds the position of the first letter after the first quote
    beginning = 0
    # Looping through current line to isolate the URL
    for i in range(0, len(a_href_line)):
        # If a double quote is found, determine whether its the first or second
        if a_href_line[i] == '"':
            # If its the first then set the appropriate variable, record where the first quote is
            if first_quote_found == False:
                first_quote_found = True
                beginning = i + 1
            # Otherwise slice the current line and record the URL part
            else:
                url = a_href_line[beginning:i]
                id = url.rpartition('/')[2].partition('?')[0]
                number = -1
                for j in id.split('-'):
                    if j.isdigit():
                        number = int(j)
                        break
                if number in download_list:
                    print('adding episode: ' + str(number))
                    video_list.insert(0, Video.Video(url, id, number))
                break
def get_url_2(a_href_line):
    parts = a_href_line.split('"')[1]
def search_for_url(website, video_list):
    episode_list = False
    for line in website:
        # If the tag that starts the list of URL's is found on this line, then state that we're inside the list and that we need to start looking for URL tags
        if '<table class="listing">' in line:
            episode_list = True
        # If the tag that ends the list is found, then stop looking
        if '</tbody></table>' in line and episode_list:
            break
        # If the line we're currently looking at has the link tag, then start isolating the URL
        if episode_list and '<a href="' in line:
            # Making a copy of the line
            a_href_line = (line + '.')[:-1]
            get_url(video_list, a_href_line)

def get_episode_list_page(webpage_input):
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(webpage_input)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'ul')))
    return driver.page_source
    driver.close()
    #print(driver.find_element_by_tag_name('body'))

def get_video(video_list):
    dlq = []
    video_log_file = open('finished_video_list.txt', 'r+')
    for video in video_list:
        found = False
        for line in video_log_file:
            line = line.rstrip('\n')
            print('LINE = ' + line)
            if line in video.get_web_page_url():
                found = True
                break
        if not found:
            print('Getting a video')
            print(video.get_web_page_url())
            driver = webdriver.Chrome()
            driver.implicitly_wait(10)
            driver.get(video.get_web_page_url())
            num_attempts = 0
            while num_attempts < 4:
                try:
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.element_to_be_clickable((By.ID, 'my_video_1_html5_api')))
                    url = driver.find_element('id','my_video_1_html5_api').get_attribute('src')
                    video.set_video_page_url(url)
                    driver.close()
                    video.get_video_file()
                    break
                except TimeoutException:
                    print('Lost Connection, Attempting to re-establish...')
                    num_attempts += 1
                    if num_attempts == 4:
                        print('Skipping episode ' + video.get_id() + ' due to timeout exception.')
                        driver.close()
                        break
    video_log_file.close()


def format_input(input=''):
    download_list = []
    if input == '':
        return None
    input_split_commas = input.split(', ')
    for ep in input_split_commas:
        if '-' in ep:
            start = int(ep.split('-')[0])
            end = int(ep.split('-')[1])
            for i in range(start, end+1):
                download_list.append(i)
        else:
            download_list.append(int(ep))
    return download_list








download_list = format_input(episodes_to_download)
# Create a list that holds all the URL's for the pages of the videos (not the videos themselves)
url_list = []
video_url_list = [[]]
video_list = []
search_for_url(website, url_list)
print(url_list)
get_video(video_list)
print('Done!')
#Video.Video.video_log.close()
print(len(url_list))
#TODO: Getting episode list page through http rather than file
#TODO: Being able to enter which episodes you want
#TODO: Print which episodes werent able to download
#TODO: If program stops all of the sudden, write which episodes have finished downloading to a file for later reference