
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import Video
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

                video_list.insert(0, Video.Video(url))
                # Insert the url into the list of URL's (insert at the beginning because the website lists latest to earliest)
                #url_list.insert(0, url)
                break

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



# def get_video(url_list, video_url_list, num_episodes_per_loop):
#
#     for video_page in url_list:
#         print(video_page)
#         driver = webdriver.Chrome()
#         driver.implicitly_wait(10)
#         driver.get(video_page)
#         wait = WebDriverWait(driver, 10)
#         wait.until(EC.element_to_be_clickable((By.ID, 'my_video_1_html5_api')))
#         url = driver.find_element('id','my_video_1_html5_api').get_attribute('src')
#         video_url_list.append(url)
#         driver.close()
#         video = urllib.urlopen(url)
#         meta = video.info()
#
#         break
#     print('Video URL List: ')
#     print(video_url_list[0])

def get_video(video_list, num_episodes_per_loop):
    dlq = []
    for video in video_list:
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
                break
            except TimeoutException:
                print('Lost Connection, Attempting to re-establish...')
                num_attempts += 1
                if num_attempts == 4:
                    print('Skipping episode ' + video.get_id() + ' due to timeout exception.')


        # while True:
        #     if len(dlq) < num_episodes_per_loop:
        #         dlq.append(video)
        #         break
        #     x = False
        #     for vid in dlq:
        #         if open(str(vid.id) + '.mp4', 'r').read() >= vid.video_file_size:
        #             x = True
        #             break
        #     if x:
        #         dlq.remove(vid)
        #         break
        # print(video.get_video_page_url())
        video.get_video_file()




# url = 'https://r6---sn-cxaaj5o5q5-tt1s.googlevideo.com/videoplayback?requiressl=yes&id=46620c0175681201&itag=22&source=webdrive&app=texmex&ip=184.151.178.128&ipbits=32&expire=1464903731&sparams=expire,id,ip,ipbits,itag,mm,mn,ms,mv,pl,requiressl,source&signature=040C0DCA35A7F72C422D7CFC86963F4588C5EDD4.2A0146525ECB32FCCEF375F9C0F2262941F47672&key=cms1&pl=19&cms_redirect=yes&mm=31&mn=sn-cxaaj5o5q5-tt1s&ms=au&mt=1464892156&mv=m'
# url2 = 'http://i.imgur.com/ccVNe2b.jpg'
# file_name = 'test.jpg'
# print('Attempting to download')
# urllib.request.urlretrieve(url2, file_name)
# print("done!")

# Request the name of the file
# webpage_input = input("Enter Website: ")
# Open the file with reading permission
num_episodes_per_loop = int( input('Number of Episodes to Download at Once (higher numbers risk being caught)'))
website = open('webpage.html', 'r', encoding='utf8')
# Create a variable that states whether we have found the html list that holds the list of URL's
episode_list = False
# Create a list that holds all the URL's for the pages of the videos (not the videos themselves)
url_list = []
video_url_list = [[]]
video_list = []
search_for_url(website, url_list)
get_video(video_list, num_episodes_per_loop)
print(url_list)
print(len(url_list))