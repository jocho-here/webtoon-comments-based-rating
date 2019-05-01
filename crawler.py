import time
from selenium import webdriver
import selenium as selenium


######################################################################
########################## NEED TO TEST###############################
######################################################################
######################################################################
######################################################################
browser = webdriver.Safari()

curr_page = 'https://www.webtoons.com/en/fantasy/tower-of-god/season-1-ep-0/viewer?title_no=95&episode_no=1'
went_through_all = False
all_comments = []

while went_through_all == False:
    browser.get(curr_page)
    time.sleep(5)

    epi_comments = []
    curr_page = 1
    finished = False

    # Loop through all comment pages
    while finished == False:
        time.sleep(2)

        # Grab comments and add them to epi_comments
        print('')
        print("Current page#: ", curr_page)
        comments_wrap = browser.find_element_by_class_name('u_cbox_list')
        comment_boxes = comments_wrap.find_elements_by_tag_name('li')
        for comment_box in comment_boxes:
            try:
                txt_wrap = comment_box.find_element_by_class_name('u_cbox_contents')
            except selenium.common.exceptions.NoSuchElementException:
                print("Comment deleted")
            else:
                epi_comments.append(txt_wrap.text)
                print("Comments: ", txt_wrap.text)

        # Go to the next page
        paginate = browser.find_element_by_class_name('u_cbox_page_wrap')
        pages = paginate.find_elements_by_tag_name('a')
        next_page = None

        finished = True

        # Check if the current comment page is the last comment page by
        # checking the presence of `u_cbox_next`
        for page in pages:
            if page.get_attribute('class') == 'u_cbox_next': 
                next_page = page
                finished = False
                break

        # Go through pages
        for page in pages:
            if page.get_attribute('class') == 'u_cbox_page':
                pg_num = page.find_element_by_tag_name('span')

                if int(pg_num.text) == curr_page + 1:
                    page.click()
                    break

        if curr_page % 10 == 0:
            next_page.click()

        curr_page += 1

    # Check if this is the last episode
    tool_bar = browser.find_element_by_id('toolbar')
    divs = tool_bar.find_elements_by_tag_name('div')
    next_page_url = ''
    paginate = None

    for div in divs:
        if div.get_attribute('class') == 'paginate v2':
            paginate = div
            break

    if paginate == None:
        print("Couldn't find paginate v2")
    else:
        buttons = paginate.find_elements_by_tag_name('a')

        if len(buttons) == 1 and buttons[0].get_attribute('title') == 'Previous Episode':
            print("Last page!")
            went_through_all = True
        elif buttons[0].get_attribute('title') == 'Next Episode':
            curr_page = buttons[0].get_attribute('href')
        elif buttons[1].get_attribute('title') == 'Next Episode':
            curr_page = buttons[1].get_attribute('href')
        else:
            print('WTF')

    all_comments.append(epi_comments)

browser.quit()
