import streamlit as st

st.set_page_config(page_title="Smart Recipe Finder", layout="centered")

st.title("🍳 Smart Recipe Finder")
st.write("Get instant YouTube recipe search results for any dish!")

dish = st.text_input("Enter Dish Name", placeholder="e.g. Paneer Butter Masala")

def get_youtube_search_url(dish_name):
    query = f"{dish_name} recipe"
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
if dish:
    search_url = get_youtube_search_url(dish)
    st.success("✅ Recipe videos found!")
    st.markdown(f"🎥 [Click here to view YouTube recipes for **{dish}**]({search_url})")
    st.markdown("---")
    st.caption("Note: This opens YouTube search results in a new tab.")


