import streamlit as st
import pandas as pd
import pickle

# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'choice'
if 'wine_type' not in st.session_state:
    st.session_state.wine_type = 'Red Wine' # Default selection to ensure radio button has a default value

# Background and style modifications
st.markdown("""
    <style>
        .stApp {
            background-color: #FF69B4;  /* Pink background color */
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
    tastes_aromas_options = ["Fruity", "Spicy", "Oaky", "Herbal", "Chocolate and Coffee", "Floral"]
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
    textures_aromas_options = ["Light", "Medium", "Fulll"]
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

# Creating a dictionary for our input dataframe
features_dict = {'dry_wine': 0,
                 'sweet_wine': 0,
                 'fruity_aroma': 0,
                 'spicy_aroma': 0,
                 'herb_aroma': 0,
                 'oak_aroma': 0,
                 'chocolate_aroma': 0,
                 'floral_aroma': 0,
                 'body_light': 0,
                 'body_medium': 0,
                 'body_full': 0,
                 'wine_type': 'red'} # Default value is red wine

# Mapping wine types to the corresponding values in the dataset
wine_dict = {'Red Wine': 'red',
             'White Wine': 'white',
             'Rosé Wine': 'rose',
             'Sparkling Wine': 'sparkling',
             'Dessert Wine': 'dessert'}
wine_type_new = wine_dict[wine_type]
features_dict['wine_type'] = wine_type_new

# Changing aroma values to 1 if they appear in tastes_aromas_selected
aroma_features = ['fruity_aroma', 'spicy_aroma', 'oak_aroma', 'herb_aroma', 'chocolate_aroma', 'floral_aroma']

for aroma in tastes_aromas_selected:
    features_dict[aroma_features[tastes_aromas_selected.index[aroma]]] = 1

# Saving our features as a one-row dataframe
X_test = pd.DataFrame(features_dict)

# Loading our pickle file
model = pickle.load(open('../data/model.pkl', 'rb'))
