import streamlit as st
import streamlit_antd_components as sac
from functions.n1_Bot_Page import page1_funcs

st.set_page_config(page_title="Learning Bot", page_icon="./images/favicon.png")


# Link icon to function name.
# Icons are from: https://icons.getbootstrap.com/
icons = {
    "Bot Query": "diagram-3",
    "Bot Retraining": "file-check"
}

# Define the menu
menu_items = [
    sac.MenuItem("Home", icon="house-fill"),
    sac.MenuItem(
        "Learning Bot Tools",
        icon="binoculars-fill",
        children=[
            # Icon is the default for the children
            sac.MenuItem(subpage, icon=icons.get(subpage, "default-icon"))
            for subpage in page1_funcs.keys()
        ],
    ),
]

# Display the menu in the sidebar and get the selected item
with st.sidebar:
    # Size options are small, middle, largex
    selected_item = sac.menu(
        menu_items, format_func=lambda x: x, size="small", open_all=True
    )


# Function to display the main page
def show_main_page():
    logo, title = st.columns([0.1, 0.9])
    with logo:
        st.image("./images/brain.png")
    with title:
        st.title("Learning Bot")
    st.write(
        "RNN Training Pipeline and Streamlit interface for query and retraining."
    )
    st.write(
        "This application is written in Python using the [Streamlit](https://docs.streamlit.io) framework."
    )


# Display the selected page
if selected_item == "Home":
    show_main_page()
elif selected_item in page1_funcs:
    page1_funcs[selected_item]()
