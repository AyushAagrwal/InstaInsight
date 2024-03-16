import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Instagram username and password from environment variables
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

def instagram_login(username, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    driver.get("https://www.instagram.com/accounts/login/")

    time.sleep(5)

    username_field = driver.find_element(By.XPATH, "//input[@name='username']")
    password_field = driver.find_element(By.XPATH, "//input[@name='password']")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)

    if "login" not in driver.current_url:
        st.success("Login Successful!")
    else:
        st.error("Login Failed. Please check your credentials.")

    return driver

def navigate_to_profile(driver, profile_name):
    if "https://www.instagram.com/" in profile_name:
        driver.get(profile_name)
    else:
        driver.get(f"https://www.instagram.com/{profile_name}")


st.set_page_config(layout="wide", initial_sidebar_state="expanded",
                page_title="InstaInsight", page_icon=":camera:",
                menu_items={"Get Help": "https://www.linkedin.com/in/agarwal2001/"}
               )

st.title("Instagram Profile Information 🕵️‍♂️ 👁️‍🗨️")
profile_name = st.text_input("Enter the profile URL or Username", placeholder="Person You want to scrap").strip()
login_button = st.button("Login")

if login_button:
    driver = instagram_login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    navigate_to_profile(driver, profile_name)

    try:
        st.markdown("Trying to find profile photo")
        time.sleep(10)
        profile_photo = driver.find_element(By.XPATH, '//div[@class="_aarf"]//img')
        profile_photo_url = profile_photo.get_attribute('src')

        st.image(profile_photo_url, caption='Profile Photo', use_column_width=True)

        with open('profile_photo.jpg', 'wb') as file:
            file.write(requests.get(profile_photo_url).content)

        st.download_button(
            label="Download Profile Photo",
            data=open("profile_photo.jpg", "rb"),
            file_name=f"{profile_name}.jpg",
            mime="image/jpeg"
        )

    except NoSuchElementException:
        st.error("Profile photo not found")

    try:
        bio = driver.find_element(By.XPATH, '//div[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
        bio_text = bio.text

        followers_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[2]").text

        following_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[3]").text

        driver.find_element(By.XPATH,'(//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"])[2]').click()
        driver.implicitly_wait(10) 
        driver.find_element(By.XPATH,"(//div[@class='_a9-z'])//button[text()='About this account']").click()
        driver.implicitly_wait(5)
        date_joining=driver.find_element(By.XPATH,"(//span[@data-bloks-name='bk.components.Text'])[3]").text

        text_contents = f'Username: {profile_name}\nBio: {bio_text}\nFollowers: {followers_count}\nFollowing: {following_count}\nDate Joined: {date_joining}'

        st.download_button('Download Bio and Stats', text_contents, file_name=f'{profile_name}.txt')

    except NoSuchElementException:
        st.error("Bio, followers, or following count not found")

    try:
        private_profile_photo = driver.find_element(By.XPATH, '//div[@class="_aadm"]//img')
        private_profile_photo_url = private_profile_photo.get_attribute('src')

        st.image(private_profile_photo_url, caption='Private Profile Photo', use_column_width=True)

        with open('private_profile_photo.jpg', 'wb') as file:
            file.write(requests.get(private_profile_photo_url).content)

        st.download_button(
            label="Download Private Profile Photo",
            data=open("private_profile_photo.jpg", "rb"),
            file_name=f"{profile_name}.jpg",
            mime="image/jpeg"
        )
    except NoSuchElementException:
        st.error("Private profile photo not found")

    try:
        bio = driver.find_element(By.XPATH, '//div[@class="x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xwonja6 x1dyjupv x1onnzdu xwrz0qm xgmu61r x1nbz2ho xbjc6do"]')
        bio_text = bio.text

        followers_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[2]").text

        following_count = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[3]").text

        driver.find_element(By.XPATH,'(//div[@class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"])').click()
        driver.implicitly_wait(10) 
        driver.find_element(By.XPATH,"(//div[@class='_a9-z'])//button[text()='About this account']").click()
        driver.implicitly_wait(5)
        date_joining=driver.find_element(By.XPATH,"(//span[@data-bloks-name='bk.components.Text'])[3]").text

        text_contents = f'Username: {profile_name}\nBio: {bio_text}\nFollowers: {followers_count}\nFollowing: {following_count}\nDate Joined: {date_joining}'

        st.download_button('Download Bio and Stats', text_contents, file_name=f'{profile_name}.txt')

    except NoSuchElementException:
        st.error("Bio, followers, or following count not found")

if __name__ == "__main__":
    st.write("This is a Streamlit web app for Instagram profile information.")
