import streamlit as st

# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'choice'
if 'wine_type' not in st.session_state:
    st.session_state.wine_type = 'Red Wine' # Default selection to ensure radio button has a default value

# Background and style modifications
st.markdown("""
<style>
.stApp {
    background-image: url("https://media.istockphoto.com/id/1460836902/pt/foto/viva-magenta-color-background-close-up-of-daphne-leaves-viva-magenta-leaves-background-color.jpg?s=2048x2048&w=is&k=20&c=VYIDyXYZs2WI6V9MMAd6auDjCc8_fR0q9mPjX9ai2jE=");
    background-size: cover;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Page navigation and content rendering
if st.session_state.page == 'choice':
    st.title('Hello Streamlit!')
    st.write('This is a simple Streamlit app.')

    wine_type = st.radio(
        "Select Wine Type:",
        ('Red Wine', 'White Wine', 'Rosé Wine', 'Sparkling Wine', 'Dessert Wine'),
        index=('Red Wine', 'White Wine', 'Rosé Wine', 'Sparkling Wine', 'Dessert Wine').index(st.session_state.wine_type)
    )
    st.session_state.wine_type = wine_type

    if st.button('Show Aromas and Countries'):
        st.session_state.page = 'details'

elif st.session_state.page == 'details':
    st.markdown(f"## **You selected {st.session_state.wine_type}**!")

    # Tastes/aromas selection in two parallel columns
    st.write("Select Preferred Taste and Aromas :")
    tastes_aromas_options = ["Fruity", "Spicy", "Oaky", "Herbal", "Chocolate and Coffee", "Earthy and Mineral"]
    col1, col2 = st.columns(2)  # Create two columns
    tastes_aromas_selected = []

    # Distribute checkboxes across two columns
    for i, option in enumerate(tastes_aromas_options):
        if i % 2 == 0:
            with col1:
                if st.checkbox(option, key=option + "1"):
                    tastes_aromas_selected.append(option)
        else:
            with col2:
                if st.checkbox(option, key=option + "2"):
                    tastes_aromas_selected.append(option)

    if tastes_aromas_selected:
        st.write("You selected:", ", ".join(tastes_aromas_selected))
    else:
        st.write("No tastes or aromas selected")

    # Textures selection in two parallel columns

    st.write("Select Preferred Textures :")
    textures_aromas_options = ["Soft", "Creamy", "Structured", "Silky"]
    col1, col2 = st.columns(2)  # Create two columns
    textures_aromas_selected = []

    # Distribute checkboxes across two columns
    for i, option in enumerate(textures_aromas_options):
        if i % 2 == 0:
            with col1:
                if st.checkbox(option, key=option + "1"):
                    textures_aromas_selected.append(option)
        else:
            with col2:
                if st.checkbox(option, key=option + "2"):
                    textures_aromas_selected.append(option)

    if textures_aromas_selected:
        st.write("You selected:", ", ".join(textures_aromas_selected))
    else:
        st.write("No textures selected")

    # Price range slider
    st.write("Select Your Price Range:")
    price_range = st.slider("Price Range ($)", 0, 200, (10, 100))
    st.write(f"Your selected price range: ${price_range[0]} - ${price_range[1]}")

    # Country selector
    countries = ["Argentina", "Australia", "Chile", "France", "Germany", "Italy", "New Zealand", "Portugal", "South Africa", "Spain", "United States"]
    selected_country = st.selectbox("Select Country:", countries)
    st.write(f"You selected: {selected_country}")

    # Button to change wine type, wider appearance through column manipulation
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button
    with col3:
        if st.button('Change Wine Type', key='change_wine'):
            st.session_state.page = 'choice'
