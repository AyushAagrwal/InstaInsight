import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


def instagram_login(username, password):
    # Set up Selenium webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.instagram.com/accounts/login/")

    # Wait for page to load
    time.sleep(5)

    # Find username and password input fields and input credentials
    username_field = driver.find_element(By.XPATH, "//input[@name='username']")
    password_field = driver.find_element(By.XPATH, "//input[@name='password']")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for login process
    time.sleep(5)

    # Check if login was successful
    if "login" not in driver.current_url:
        st.success("Login Successful!")
    else:
        st.error("Login Failed. Please check your credentials.")

    return driver

# def download_profile_photo(profile_photo_url, filename):
#     response = requests.get(profile_photo_url)
#     with open(filename, 'wb') as f:
#         f.write(response.content)

def navigate_to_profile(driver, profile_name):
    # Navigate to profile URL or Username
    if "https://www.instagram.com/" in profile_name:
        driver.get(profile_name)
    else:
        driver.get(f"https://www.instagram.com/{profile_name}")


st.set_page_config(layout="wide", initial_sidebar_state="expanded",
                page_title="InstaInsight", page_icon=":camera:",
                menu_items={"Get Help": "https://www.linkedin.com/in/agarwal2001/"}
               )

# Streamlit UI
st.title("Instagram Login 🕵️‍♂️ 👁️‍🗨️")
username = st.text_input("Username",placeholder="Your Instagram Username").strip()
password = st.text_input("Password", type="password",placeholder="Your Instagram Password").strip()
profile_name = st.text_input("Enter the profile URL or Username",placeholder="Person You want to scrap").strip()
login_button = st.button("Login")

if login_button:
    driver = instagram_login(username, password)
    navigate_to_profile(driver, profile_name)

    try:
        st.markdown("Trying to find profile photo")
        time.sleep(10)
        # Try to find the profile photo element
        profile_photo = driver.find_element(By.XPATH, '//div[@class="_aarf"]//img')
        profile_photo_url = profile_photo.get_attribute('src')

        # Display the profile photo
        st.image(profile_photo_url, caption='Profile Photo', use_column_width=True)

        # Download the profile photo
        with open('profile_photo.jpg', 'wb') as file:
            file.write(requests.get(profile_photo_url).content)

        st.download_button(
            label="Download Profile Photo",
            data=open("profile_photo.jpg", "rb"),
            file_name="profile_photo.jpg",
            mime="image/jpeg"
        )

    except NoSuchElementException:
        st.error("Profile photo not found")

    try:
        # Get bio
        bio = driver.find_element(By.XPATH, '//div[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
        # print(bio.text)        
        bio_text = bio.text

        # Get followers count
        followers_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[2]").text

        # Get following count
        following_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[3]").text


        ## Date of joining
        driver.find_element(By.XPATH,'(//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"])[2]').click() #clicking on right three dots
        driver.implicitly_wait(10) 
        driver.find_element(By.XPATH,"(//div[@class='_a9-z'])//button[text()='About this account']").click() ##clicking on about this account
        driver.implicitly_wait(5)
        date_joining=driver.find_element(By.XPATH,"(//span[@data-bloks-name='bk.components.Text'])[3]").text

         # Create text content
        text_contents = f'Username: {profile_name}\nBio: {bio_text}\nFollowers: {followers_count}\nFollowing: {following_count}\nDate Joined: {date_joining}'

        # Download the text content as a text file
        st.download_button('Download Bio and Stats', text_contents, file_name='bio_and_stats.txt')

    except NoSuchElementException:
        st.error("Bio, followers, or following count not found")

    try:
        # Try to find the private profile photo element
        private_profile_photo = driver.find_element(By.XPATH, '//div[@class="_aadm"]//img')
        private_profile_photo_url = private_profile_photo.get_attribute('src')

        # Display the private profile photo
        st.image(private_profile_photo_url, caption='Private Profile Photo', use_column_width=True)

        # Download the private profile photo
        with open('private_profile_photo.jpg', 'wb') as file:
            file.write(requests.get(private_profile_photo_url).content)

        st.download_button(
            label="Download Private Profile Photo",
            data=open("private_profile_photo.jpg", "rb"),
            file_name="private_profile_photo.jpg",
            mime="image/jpeg"
        )
    except NoSuchElementException:
        st.error("Private profile photo not found")

    try:
        # Get bio
        bio = driver.find_element(By.XPATH, '//div[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
        # print(bio.text)        
        bio_text = bio.text

        # Get followers count
        followers_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[2]").text

        # Get following count
        following_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[3]").text


        ## Date of joining
        driver.find_element(By.XPATH,'(//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"])').click() #clicking on right three dots
        driver.implicitly_wait(10) 
        driver.find_element(By.XPATH,"(//div[@class='_a9-z'])//button[text()='About this account']").click() ##clicking on about this account
        driver.implicitly_wait(5)
        date_joining=driver.find_element(By.XPATH,"(//span[@data-bloks-name='bk.components.Text'])[3]").text

         # Create text content
        text_contents = f'Username: {profile_name}\nBio: {bio_text}\nFollowers: {followers_count}\nFollowing: {following_count}\nDate Joined: {date_joining}'

        # Download the text content as a text file
        st.download_button('Download Bio and Stats', text_contents, file_name='bio_and_stats.txt')

    except NoSuchElementException:
        st.error("Bio, followers, or following count not found")

# Keep Streamlit running until user closes the page
if __name__ == "__main__":
    st.write("This is a Streamlit web app for Instagram profile information.")