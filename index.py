
import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(
    page_title="Profit Sentinel",
    page_icon="Images/logo.png",
    layout="wide",    
    initial_sidebar_state="auto"       
)

# CSS to set background color
page_bg_color = """
<style>
    body {
        background-color: #f0f8ff; /* Light blue background */
    }
</style>
"""

# Inject CSS into the app
st.markdown(page_bg_color, unsafe_allow_html=True)
# Streamlit Title
#st.title("Profit Sentinel")

nav = get_nav_from_toml()

pg = st.navigation(nav)

add_page_title(pg)

pg.run()

def main():    
    # Load and display sidebar image
    add_logo("Images/logo.png", height=280)    
    # Add a True/False slider to the sidebar
# debug = st.sidebar.checkbox("Debug", value=False)
# if debug:
#     st.write("The checkbox in the sidebar is **checked**.")
# else:
#     st.write("The checkbox in the sidebar is **not checked**.")
# st.session_state["Debug"]=debug
main()


