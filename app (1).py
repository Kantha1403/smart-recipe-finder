import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Smart Recipe Finder", layout="centered")

def get_youtube_link(dish_name):
    try:
        query = f"{dish_name} recipe site:youtube.com"
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "/watch?v=" in href:
                return "https://www.youtube.com" + href
        return None
    except Exception as e:
        st.error(f"Error fetching YouTube video: {e}")
        return None

st.title("🍳 Smart Recipe Finder")

st.write("Get a YouTube recipe video instantly — no APIs, no CSVs!")

dish = st.text_input("Enter Dish Name (e.g., Paneer Butter Masala):")
if dish:
    with st.spinner("🔎 Searching YouTube..."):
        video_link = get_youtube_link(dish)
    if video_link:
        st.success("✅ Found a YouTube recipe!")
        st.video(video_link)
    else:
        st.error("❌ No recipe video found. Try another dish.")


