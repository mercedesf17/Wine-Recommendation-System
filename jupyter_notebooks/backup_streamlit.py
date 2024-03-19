import streamlit as st

import plotly.graph_objects as go

import pandas as pd

from models import *
from dataframing import *
import base64
import pydeck as pdk
from math import radians, cos, sin, asin, sqrt


# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'begin'


st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/fUHxmyW.png");  /* Pink background color */
            background-size: cover;
            }
        .sidebar .sidebar-content {
            background-color: #fcb1b9;
        }
    </style>
    """, unsafe_allow_html=True)

# Title page
if st.session_state.page == 'begin':

    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
        .custom-font {
            font-family: 'Lobster', cursive;
            text-align: center;
            color: #333;
            font-size: 2.5em;
        }
    </style>
""", unsafe_allow_html=True)

    st.markdown("<h1 class='custom-font'>Wine Whisperer</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style = 'text-align: center; color: black;'> Unveiling Flavorful Secrets 🍷🍇</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button('Begin 🥂'):
            st.session_state.page = 'choice'

# First page, choosing wine type
elif st.session_state.page == 'choice':
    st.markdown("<h3 style = 'text-align: center; color: black;'> Please select your preferred wine type:</h3>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
    }
    </style>
""",unsafe_allow_html=True)

    wine_type = st.radio(
        label = "Select Wine Type:",
        label_visibility = 'hidden',
        options = ('Red Wine', 'White Wine', 'Rosé Wine', 'Sparkling Wine', 'Dessert Wine'),
        index=0,
        horizontal = True)
    st.session_state.wine_type = wine_type

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button('Continue 🥂'):
            st.session_state.page = 'flavors'

# Second page for flavor profiles
elif st.session_state.page == 'flavors':
    st.markdown(f"<h3 style = 'text-align: center; color: black;'> You selected: {st.session_state.wine_type}!</h3> ", unsafe_allow_html=True)

    st.markdown("<h3 style = 'text-align: center; color: black;'> Please select your preferred flavor and texture profile:</h3>", unsafe_allow_html=True)

    # Dryness options as a radio button
    st.markdown("""<style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
        font-size: 30px;
        gap: 20rem;
    }
    </style>""",
    unsafe_allow_html=True)

    dryness_selected = st.radio(
        label = 'Please select your preferred dryness:',
        options = ('Dry', 'Sweet'),
        index = None,
        horizontal = True
    )
    st.session_state.dryness_selected = dryness_selected

    if dryness_selected:
        st.write(f"You selected: {dryness_selected}")
    else:
        st.write("No dryness selected")

    # Aromas selection in two parallel columns
    st.write("Please select your preferred aromas:")
    tastes_aromas_options = ["Fruity", "Spiced", "Oaky", "Herbal", "Chocolate and Coffee", "Floral"]
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

    st.session_state.tastes_aromas_selected = tastes_aromas_selected

    # Body selection in two parallel columns
    st.write("Please select your preferred body:")
    textures_aromas_options = ["Light", "Medium", "Full"]
    col1, col2 = st.columns(2)  # Create two columns
    body_selected = []

    # Distribute checkboxes across two columns
    for i, option in enumerate(textures_aromas_options):
        if i % 2 == 0:
            with col1:
                if st.checkbox(option, key=option + "1"):
                        body_selected.append(option)
        else:
            with col2:
                if st.checkbox(option, key=option + "2"):
                    body_selected.append(option)

    if body_selected:
        st.write("You selected:", ", ".join(body_selected))
    else:
        st.write("No body selected")
    st.session_state.body_selected = body_selected

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button('Continue 🍾'):
            st.session_state.page = 'price'

elif st.session_state.page == 'price':
    # Price range slider
    st.markdown("<h3 style = 'text-align: center; color: black;'> Please select your preferred price range (in USD):</h3>", unsafe_allow_html=True)

    price_range = st.slider(label = "Price Range ($)",
                            min_value = 0,
                            max_value = 200,
                            value = (10, 100))

    st.write(f"Your selected price range is: \${price_range[0]} - \${price_range[1]}")

    st.session_state.price_range = price_range

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        if st.button("Continue 🍷"):
            st.session_state.page = 'country'

elif st.session_state.page == 'country':

    # Country selector
    countries = ["Portugal", "Spain", "France", "Germany", "Austria",
                "Italy", "Greece", "Israel", "South Africa", "Australia",
                "New Zealand", "Chile", "Argentina", "US", "Canada"]
    selected_country = st.selectbox("Select Country:", countries)
    st.write(f"You selected: {selected_country}")

    st.session_state.selected_country = selected_country



    # Mapping wine types to the corresponding values in the dataset
    wine_type = st.session_state.wine_type if 'wine_type' in st.session_state else 'Red Wine'
    wine_dict = {'Red Wine': 'red',
                'White Wine': 'white',
                'Rosé Wine': 'rose',
                'Sparkling Wine': 'sparkling',
                'Dessert Wine': 'dessert'}
    wine_type_new =  wine_dict.get(wine_type, 'red')

    dryness_selected = st.session_state.dryness_selected if 'dryness_selected' in st.session_state else None

    tastes_aromas_selected = st.session_state.tastes_aromas_selected if 'tastes_aromas_selected' in st.session_state else []

    body_selected = st.session_state.body_selected if 'body_selected' in st.session_state else []

    price_range = st.session_state.price_range if 'price_range' in st.session_state else (10, 100)

    selected_country = st.session_state.selected_country if 'selected_country' in st.session_state else 'Portugal'

    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button

    with col2:

        if st.button('Get Recommendations', key='get_recommendations'):
        # Updating the features dictionary
            features_dict = update_dryness(dryness_selected)
            features_dict = update_aromas(tastes_aromas_selected, features_dict)
            features_dict = update_body(body_selected, features_dict)
            features_dict = update_country(selected_country, features_dict)

        # Creating a DataFrame for the input features
            X_test = pd.DataFrame(features_dict, index=[0])

        # Initiating and training the model
            filtered = filtered_rows(price_range, wine_type_new)
            model = train_model(filtered)

        # Get the recommended wines by calling the match_type and describe functions from models
            recommendations = neighbors(model, filtered, X_test)
            recommendations['rank'] = range(1, len(recommendations) + 1)
            st.session_state.recommendations = recommendations

            descriptions = describe(recommendations)
            st.session_state.descriptions = descriptions

            st.session_state.page = 'loading'

elif st.session_state.page == 'loading':
    st.markdown("<h3 style = 'text-align: center; color: black;'>Our wine whisperer is searching... Stay tuned!</h3>", unsafe_allow_html=True)
    st.image('data/hello catherine.png')

    col1, col2, col3, col4, col5 = st.columns([1, 1, 3, 1, 1])
    with col3:
        if st.button('Show Recommendations 🍷'):
            st.session_state.page = 'recommendations'

elif st.session_state.page == 'recommendations':

    recommendations = st.session_state.recommendations
    descriptions = st.session_state.descriptions

    # Mapping function
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great-circle distance between two points on the Earth's surface.
        """
    # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        distance = c * r

        return distance

    def calculate_zoom_level(lon_range, lat_range, width, height, max_zoom=4):

        """
        Calculate the appropriate zoom level based on the haversine distance and map dimensions.
        """
        max_lon_distance = haversine(lon_range[0], lat_range[0], lon_range[1], lat_range[0])
        max_lat_distance = haversine(lon_range[0], lat_range[0], lon_range[0], lat_range[1])

        if max_lon_distance == 0 or max_lat_distance == 0:
        # Handle the case where distances are zero to avoid division by zero
            return max_zoom

    # Adjust these factors based on your preference
        zoom_x_factor = 0.3
        zoom_y_factor = 0.3

        additional_zoom_factor = 0.5  # Experiment with different values



    # Assume that the screen width corresponds to 256 pixels at zoom level 1
        screen_width = 256
        zoom_x = (360 * (width / screen_width)) / (max_lon_distance * zoom_x_factor)
        zoom_y = (170 * (height / screen_width)) / (max_lat_distance * zoom_y_factor)

    # Use the minimum zoom level to fit both x and y directions
        zoom_level = min(zoom_x, zoom_y)
        zoom_level = min(zoom_level, max_zoom)

        return zoom_level

    def animated_map(X: pd.DataFrame):
    # Calculate the bounding box
        lon_range = [X['lon'].min(), X['lon'].max()]
        lat_range = [X['lat'].min(), X['lat'].max()]

    # Calculate the appropriate zoom level
        zoom_level = calculate_zoom_level(lon_range, lat_range, 800, 600)  # Adjust map dimensions as needed

    # Create a PyDeck scatter plot layer
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=X,
            get_position=['lon', 'lat'],
            get_radius=50000,
            get_fill_color=[187, 19, 47, 160],  # RGBA color with alpha transparency
            pickable=True,
            auto_highlight=True
        )

    # Create a PyDeck deck with the scatter plot layer
        deck = pdk.Deck(
            map_style='mapbox://styles/mapbox/satellite-v9',
            initial_view_state=pdk.ViewState(
                latitude=(lat_range[0] + lat_range[1]) / 2,
                longitude=(lon_range[0] + lon_range[1]) / 2,
                zoom=zoom_level,
                pitch=0
            ),
            layers=[scatter_layer],
            tooltip={'text': '{rank}, {region}, {province}'}
        )

    # Display the PyDeck deck
        st.pydeck_chart(deck)



    # Display the PyDeck deck

# Example usage:
# animated_map(your_dataframe)


    # Show the choices
    dryness_selected = st.session_state.dryness_selected.lower() if st.session_state.dryness_selected else ''
    wine_type = st.session_state.wine_type.lower() if 'wine_type' in st.session_state else 'red wine'
    tastes_aromas_selected = 'with '+', '.join(st.session_state.tastes_aromas_selected).lower()+' aromas' if st.session_state.tastes_aromas_selected != [] else ''
    body_selected = 'and '+', '.join(st.session_state.body_selected).lower()+' body' if st.session_state.body_selected != [] else ''
    selected_country = st.session_state.selected_country if 'selected_country' in st.session_state else 'Portugal'
    price_range = st.session_state.price_range if 'price_range' in st.session_state else (10, 100)

    st.markdown(f"<h4 style = 'text-align: center; color: black;'>\
        You chose a {dryness_selected} {wine_type} \
            {tastes_aromas_selected} {body_selected} from {selected_country}\
                in the price range of ${price_range[0]} - ${price_range[1]}\
                    </h4>", unsafe_allow_html=True)

    # Display the recommendations and the map
    st.markdown("<h3 style = 'text-align: center; color: black;'>Recommended Wines:</h3>", unsafe_allow_html=True)
    st.write('\n'.join(descriptions))
    #st.plotly_chart(plotly_map(recommendations))
    animated_map(recommendations)
