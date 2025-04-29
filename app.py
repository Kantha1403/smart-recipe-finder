import streamlit as st
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re

# === Setup ===
st.set_page_config(page_title="Smart Recipe Finder", page_icon="🍳", layout="centered")
st.title("🍳 Smart Recipe Finder")
st.caption("Searches recipes from real sites or YouTube. No AI, no API key needed!")

# === Helpers ===
def remove_non_ascii(text):
    return ''.join(c for c in text if ord(c) < 128)

def filter_ingredients(raw_lines):
    ingredients = []
    pattern = re.compile(r"\d.*(tsp|tbsp|cup|g|ml|kg|oz|litre|teaspoon|tablespoon|gram|pound)", re.I)
    for line in raw_lines:
        if pattern.search(line):
            ingredients.append(line.strip())
    return ingredients

# === Web Recipe Search ===
def fetch_recipe_google(dish, diet_choice):
    try:
        query = f"{dish} recipe"
        if diet_choice == "🥗 Veg Only":
            query += " vegetarian"
        elif diet_choice == "🍖 Non-Veg Only":
            query += " chicken OR egg OR mutton OR fish"

        query += " site:allrecipes.com OR site:tarladalal.com OR site:hebbarskitchen.com"

        urls = list(search(query, num_results=5))
        for url in urls:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.content, "html.parser")
            text = soup.get_text(separator="\n")
            lines = text.split("\n")
            lines = [l.strip() for l in lines if len(l.strip()) > 5]

            ingredients = filter_ingredients(lines)
            steps = [line for line in lines if line.lower().startswith(tuple("123456789")) or "step" in line.lower()]

            if len(ingredients) >= 3 and len(steps) >= 3:
                return url, ingredients[:15], steps[:15]
    except Exception as e:
        st.warning(f"Error during recipe search: {e}")
    return None, [], []

# === YouTube Recipe Fallback ===
def get_youtube_link(dish, diet_choice):
    query = f"{dish} recipe"
    if diet_choice == "🥗 Veg Only":
        query += " vegetarian"
    elif diet_choice == "🍖 Non-Veg Only":
        query += " chicken OR egg OR mutton OR fish"
    query += " site:youtube.com"

    for url in search(query, num_results=5):
        if "youtube.com/watch" in url:
            return url
    return None

# === Streamlit UI ===
with st.form("recipe_form"):
    dish = st.text_input("Enter dish name", placeholder="e.g. Veg Fried Rice")
    diet_choice = st.radio("Select Dish Type:", ["🍽️ Both", "🥗 Veg Only", "🍖 Non-Veg Only"])
    video_only = st.checkbox("🎥 Show only YouTube recipes")
    submitted = st.form_submit_button("Find Recipe")

# === Handle Search ===
if submitted:
    if not dish:
        st.warning("Please enter a dish name.")
    else:
        st.info("🔎 Searching for recipes...")

        if video_only:
            yt_link = get_youtube_link(dish, diet_choice)
            if yt_link:
                st.success("🎥 Found a YouTube recipe!")
                st.markdown(f"[👉 Watch on YouTube]({yt_link})")
            else:
                st.error("❌ No YouTube recipe found.")
        else:
            url, ingredients, steps = fetch_recipe_google(dish, diet_choice)

            if ingredients and steps:
                st.success("✅ Recipe Found!")
                st.markdown(f"📎 [Source Website]({url})")

                st.markdown("### 🧂 Ingredients")
                for item in ingredients:
                    st.markdown(f"- {remove_non_ascii(item)}")

                st.markdown("### 👨‍🍳 Instructions")
                for i, step in enumerate(steps, 1):
                    st.markdown(f"{i}. {remove_non_ascii(step)}")
            else:
                yt_link = get_youtube_link(dish, diet_choice)
                if yt_link:
                    st.warning("⚠️ Couldn't find a text recipe. Here's a YouTube video instead:")
                    st.markdown(f"[👉 Watch on YouTube]({yt_link})")
                else:
                    st.error("❌ No recipe found online.")

