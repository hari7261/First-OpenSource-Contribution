import streamlit as st
from scraper import scrape_metadata
from database import init_db, insert_metadata, fetch_all_metadata

# Initialize DB
init_db()

st.set_page_config(page_title="Website Metadata Scraper", layout="centered")

st.title("🌐 Website Metadata Scraper")

url = st.text_input("Enter Website URL (with https://)")

if st.button("Scrape Metadata"):
    if url:
        data, error = scrape_metadata(url)
        if error:
            st.error(error)
        else:
            st.success("Metadata Scraped Successfully!")
            st.json(data)
            insert_metadata(data)
    else:
        st.warning("Please enter a valid URL!")

st.markdown("---")
st.subheader("📦 Stored Metadata History")

records = fetch_all_metadata()
for record in records:
    st.markdown(f"""
    - **URL**: {record[1]}
    - **Title**: {record[2]}
    - **Description**: {record[3]}
    - **Keywords**: {record[4]}
    - **OG Title**: {record[5]}
    ---
    """)
