from itertools import cycle
import os
import requests
import streamlit as st
from PIL import Image
from annotated_text import annotated_text
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu


def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'logo.ico'))
    st.set_page_config(page_title='COVID-DASHBOARD', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    body {
      background: #f4f4f4;
    }
    
    .banner {
      background: #a770ef;
      background: -webkit-linear-gradient(to right, #a770ef, #cf8bf3, #fdb99b);
      background: linear-gradient(to right, #a770ef, #cf8bf3, #fdb99b);
    }       
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

    st.balloons()
    # I want it to show balloon when it finished loading all the configs


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def remote_js(url):
    st.markdown(f'<script src={url} ></script', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


def zim_news_top_stories(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all(class_="hentry sirius-card")
    aggregates = []

    for article in articles:
        links = [i['href'] for i in article.select('a')]
        titles = [i.get('alt') for i in article.select('link')]
        image = [i['data-src'] for i in article.select('img')]
        content = [i.text for i in article.select('p')]
        aggregates.append([links[0], titles[0], image[0], content[0]])
    return aggregates


def home():
    st.header("Zim Top Stories")
    newspapers = ["Herald Zimbabwe", "Sunday Mail", "Hmetro", "Chronicle", "Suburban", "Manica Post"]
    col1,col2=st.columns(2)
    with col1:
        option = st.selectbox('please newspaper?', (newspapers), help="Please select newspaper")
        annotated_text(
            ("", option)
        )



    remote_css("https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css")
    remote_css("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.min.css")
    remote_js("https://code.jquery.com/jquery-3.3.1.slim.min.js")
    remote_js("https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/js/bootstrap.bundle.min.js")
    if option == "Herald Zimbabwe":
        fetch_articles('https://www.herald.co.zw/category/articles/top-stories')

    elif option == "Sunday Mail":
        fetch_articles('https://www.sundaymail.co.zw/category/news/top-stories')

    elif option == "Hmetro":
        fetch_articles('https://www.hmetro.co.zw/category/top-stories/')

    elif option == "Chronicle":
        fetch_articles('https://www.chronicle.co.zw/category/s6-demo-section/c37-top-stories/')

    elif option == "Suburban":
        fetch_articles('https://www.suburban.co.zw/category/top-stories/')

    elif option == "Manica Post":
        fetch_articles('https://www.manicapost.co.zw/category/top-stories/')

def fetch_articles(url):
    data = (zim_news_top_stories(url))
    st.markdown(f"""
                            <div class="container-fluid">
                                  <div class="mt-1">
                                    <!-- For demo purpose -->
                                    <div class="row py-3">
                                      <div class="col-lg-12 mx-auto">
                                        <div class="text-white p-2 shadow-sm rounded banner">
                                          <p class="lead">
                                          Webscrapping covid top stories & other news for zim leading newspapers
                                          </p>
                                        </div>
                                      </div>
                                    </div>
                            </div>
                        </div>""", unsafe_allow_html=True)

    cols = cycle(st.columns(4))
    for i, top_story in enumerate(data):

        try:
            img = Image.open(requests.get(top_story[2].encode('utf-8').strip(), stream=True).raw)
            next(cols).image(img, width=150, caption=top_story[1] + "\n\n" + top_story[0])


        except:
            next(cols).image("./components/img/logo.ico", width=150, caption=top_story[1] + "\n\n" + top_story[0])


def other_tab():
    st.header("Other TAB")


def main():
    config()
    with st.sidebar:
        choice = option_menu("Main Menu", ["Home", 'Other Tab'], icons=['house', 'list-task'], menu_icon="cast",
                             default_index=0)

    home() if (choice == "Home") else other_tab()

if __name__ == '__main__':
    main()
