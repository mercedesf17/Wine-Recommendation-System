import streamlit as st

import pandas as pd
import numpy as np

from models import *
from dataframing import *
import pydeck as pdk



# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'begin'

# Background and style modifications
st.markdown("""
        <style>
            .stApp {
                background-image: url("https://i.imgur.com/fUHxmyW.png");
                background-size: cover;
            }
            .content-area, .block-container {
                background-color: rgba(2, 2, 0, 0.75); /* Semi-transparent black */
                color: white; /* Adjust text color to improve readability */
            }
            .st-bq {
                color: white;
            }
            .st-be {
                background-color: rgb(250, 170, 186)
            }
            .st-eq {
                background-color: rgb(250, 170, 186)
            }
            .st-er {
                background-color: rgb(250, 170, 186)
            }
            .st-emotion-cache-2n7b7j {
                background: rgb(250, 170, 186)
            }
            .st-emotion-cache-l9bjmx p {
                font-size: 20px;
            }
</style>
""", unsafe_allow_html=True)


# Title page
if st.session_state.page == 'begin':
    st.markdown("<h1 style = 'text-align: center;\
                color: white; \
                font-family: Domino;'>\
                Wine Whisperer </h1>", unsafe_allow_html=True)
    st.markdown("<h2 style = 'text-align: center;\
                color: white;\
                font-family: Apple Chancery, crusive;'>\
                Unveiling Flavorful Secrets 🍷🍇</h2>",
                unsafe_allow_html=True)

    # Adding a button to start the process
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Begin 🥂')

    if button:
        st.session_state.page = 'choice'
        st.experimental_rerun()

# First page, choosing wine type
elif st.session_state.page == 'choice':
    st.markdown("<h3 style = 'text-align: center; color: white;'> Please select your preferred wine type:</h3>", unsafe_allow_html=True)

    # Adding a radio button to select the wine type
    st.markdown("""
    <style>
        .stRadio [role=radiogroup] {
            align-items: center;
            justify-content: center;
            color: white;
        }
        .stRadio input[type="radio"] + label {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


    wine_type = st.radio(
        label = "Select Wine Type:",
        label_visibility = 'hidden',
        options = ('Red Wine', 'White Wine', 'Rosé Wine', 'Sparkling Wine', 'Dessert Wine'),
        index=0,
        horizontal = True)
    st.session_state.wine_type = wine_type

    # Adding a button to continue to next page
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Continue 🥂')

    if button:
            st.session_state.page = 'flavors'
            st.experimental_rerun()

# Second page for flavor profiles
elif st.session_state.page == 'flavors':
    st.markdown(f"<h3 style = 'text-align: center; color: white;'> You selected: {st.session_state.wine_type}!</h3> ", unsafe_allow_html=True)

    st.markdown("<h3 style = 'text-align: center; color: white;'> Please select your preferred flavor and texture profile:</h3>", unsafe_allow_html=True)

    # Dryness options as a radio button
    st.markdown("""<style>
    .stRadio [role=radiogroup] {
        align-items: center;
        justify-content: center;
        gap: 10rem;
    }
    .stRadio label {
        font-size: 20px;
        color: #faaaba;
    }
    </style>""",
    unsafe_allow_html=True)


    text_color = "#ffffff"  # Change this to the desired text color


    dryness_selected = st.radio(
        label = 'Please select your preferred dryness:',
        options = ('Dry', 'Sweet'),
        index = None,
        horizontal = True
        )

    text_style = f'<style>div.stRadio label span {{ color: {text_color}; }}</style>'
    st.markdown(text_style, unsafe_allow_html=True)

    st.session_state.dryness_selected = dryness_selected

    if dryness_selected:
        st.markdown(f"<p style = 'text-align: center;'>You selected: {dryness_selected}</p>", unsafe_allow_html=True)
    else:
        st.write("<p style = 'text-align: center;'>No dryness selected</p>", unsafe_allow_html=True)

    # Aromas selection in two parallel columns
    st.markdown('#') #line of empty space
    st.markdown("<span style = 'font-size: 20px; color: #faaaba'>Please select your preferred aromas:</span>", unsafe_allow_html=True)
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
        st.markdown(f"<p style = 'text-align: center;'>You selected: {', '.join(tastes_aromas_selected)}</p>", unsafe_allow_html=True)
    else:
        st.write("<p style = 'text-align: center;'>No tastes or aromas selected</p>", unsafe_allow_html=True)

    st.session_state.tastes_aromas_selected = tastes_aromas_selected

    # Body options as a radio button
    st.markdown("""<style>
    .stRadio [role=radiogroup] {
        align-items: center;
        justify-content: center;
        gap: 10rem;
    }
    .stRadio label {
        font-size: 20px;
        color: #faaaba;
    }
    </style>""",
    unsafe_allow_html=True)

    body_selected = []


    body_selected_radio = st.radio(
        label = 'Please select your preferred body:',
        options = ('Light', 'Medium', 'Full'),
        index = None,
        horizontal = True
        )

    text_style = f'<style>div.stRadio label span {{ color: {text_color}; }}</style>'
    st.markdown(text_style, unsafe_allow_html=True)

    if body_selected_radio:
        st.write(f"<p style = 'text-align: center;'>You selected: {body_selected_radio}</p>", unsafe_allow_html=True)
        body_selected.append(body_selected_radio)
    else:
        st.write("<p style = 'text-align: center;'>No body selected</p>", unsafe_allow_html=True)

    st.session_state.body_selected = body_selected

    # Adding a button to continue to next page
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Continue 🍾')

    if button:
        st.session_state.page = 'price'
        st.experimental_rerun()

elif st.session_state.page == 'price':
    # Price range slider
    st.markdown("<h3 style = 'text-align: center; color: white;'> Please select your preferred price range (in USD):</h3>", unsafe_allow_html=True)

    st.markdown("""
                <style>
                div.stSlider label {
                    text-align: center;
                    font-size: 30px;
                    color: white}
                </style>""", unsafe_allow_html=True)

    price_range = st.slider(label = "Price Range ($)",
                            min_value = 0,
                            max_value = 200,
                            value = (10, 100))

    st.write(f"<p style = 'text-align: center;'>Your selected price range is: ${price_range[0]} - ${price_range[1]}</p>", unsafe_allow_html=True)

    st.session_state.price_range = price_range

    # Adding a button to continue to next page
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Continue 🍷')

    if button:
        st.session_state.page = 'country'
        st.experimental_rerun()

elif st.session_state.page == 'country':

    # Country selector
    countries = ["Portugal", "Spain", "France", "Germany", "Austria",
                "Italy", "Greece", "Israel", "South Africa", "Australia",
                "New Zealand", "Chile", "Argentina", "US", "Canada"]

    st.markdown("<h3 style = 'text-align: center; color: white;'>Please select a preferred country:</h3>", unsafe_allow_html=True)

    st.markdown("""
                <style>
                div.stSelectbox label {
                    text-align: center;
                    font-size: 30px;
                    color: white}
                div[role="listbox"] ul {
                    background-color: black;
                    }
                </style>""", unsafe_allow_html=True)

    selected_country = st.selectbox("Select Country",countries)
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

    # Adding a button to get recommendations
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Get Recommendations 🍇')

    if button:
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
        st.experimental_rerun()

elif st.session_state.page == 'loading':
    st.markdown("<h3 style = 'text-align: center; color: white;'>Our wine whisperer is searching... Stay tuned!</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,8,1])

    with col2:
        st.image("https://i.imgur.com/XzEhm9x.png")

    # Adding a button to show recommendations
    st.markdown("""
                <style>
                div.stButton {text-align:center; color: black}
                </style>""", unsafe_allow_html=True)
    button = st.button('Show Recommendations 🍷')

    if button:
        st.session_state.page = 'recommendations'
        st.experimental_rerun()

elif st.session_state.page == 'recommendations':

    recommendations = st.session_state.recommendations
    descriptions = st.session_state.descriptions

    # Functions

    ## Mapping functions

    ### Haversine distance
    def haversine(lon1: float, lat1: float,
                  lon2: float, lat2: float) -> float:
        """
        Calculate the great-circle distance between two points on the Earth's surface.
        """
    # Convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        distance = c * r

        return distance

    ### Calculate zoom level
    def calculate_zoom_level(lon_range: list, lat_range: list,
                             width: int, height: int, max_zoom=4) -> float:
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

    ### Plots animated map
    def animated_map(X: pd.DataFrame):
        """Plots an animated map with the coordinated in the input dataframe
    using pydeck """
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
            map_style='mapbox://styles/mapbox/outdoors-v11',
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

    ## Emojis

    ### Gets the country of a wine and returns an emoji flag
    def emoji_flag(df: pd.DataFrame) -> str:
        '''Takes a single row of a DataFrame as input and returns the emoji flag
        of the rows country'''
        flags_dict = {'US': '🇺🇸',
                      'France': '🇫🇷',
                      'Italy': '🇮🇹',
                      'Spain': '🇪🇸',
                      'Portugal': '🇵🇹',
                      'Chile': '🇨🇱',
                      'Argentina': '🇦🇷',
                      'Austria': '🇦🇹',
                      'Australia': '🇦🇺',
                      'Germany': '🇩🇪',
                      'New Zealand': '🇳🇿',
                      'South Africa': '🇿🇦',
                      'Israel': '🇮🇱',
                      'Greece': '🇬🇷',
                      'Canada': '🇨🇦'}

        country = df['country']
        flag = flags_dict[country]

        return flag

    ### Returns a digit as an emoji
    def emoji_num(n: int) -> str:
        '''Takes a number as input and returns the corresponding emoji'''
        emoji_nums = {0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣',
                      5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'}
        num = emoji_nums[n]

        return num

    # Show the choices

    ## Turning session state choice variables into appropriate strings
    dryness_selected = st.session_state.dryness_selected.lower() if st.session_state.dryness_selected else ''
    wine_type = st.session_state.wine_type.lower() if 'wine_type' in st.session_state else 'red wine'
    tastes_aromas_selected = 'with '+', '.join(st.session_state.tastes_aromas_selected).lower()+' aromas' if st.session_state.tastes_aromas_selected != [] else ''
    body_selected = ', '.join(st.session_state.body_selected).lower()+'-bodied' if st.session_state.body_selected != [] else ''
    selected_country = st.session_state.selected_country if 'selected_country' in st.session_state else 'Portugal'
    price_range = st.session_state.price_range if 'price_range' in st.session_state else (10, 100)

    ## Printing
    st.markdown(f"<h4 style = 'text-align: center; color: white;'>\
        You chose a {body_selected} {dryness_selected} {wine_type} \
            {tastes_aromas_selected} from {selected_country}\
                in the price range of ${price_range[0]} - ${price_range[1]}\
                    </h4>", unsafe_allow_html=True)

    # Display the recommendations and the map
    st.markdown("<h3 style = 'text-align: center; color:white;'>Recommended Wines:</h3>", unsafe_allow_html=True)

    for i in range(len(descriptions)):
        with st.expander(f"Recommendation {emoji_num(i+1)} {emoji_flag(recommendations.iloc[i])} \n\n{descriptions[i][0]}"):
            st.write(f"<p style = 'text-align: left; color: white ; font-size: 20px;'><b>💸  {descriptions[i][1]}</b></p>", unsafe_allow_html=True)
            st.write(f"<p style = 'text-align: left; color: white; font-size: 20px;'><b>🗺️   {descriptions[i][2]}</b></p>", unsafe_allow_html=True)
            st.write("\n\n")
            for desc in descriptions[i][3]:
                st.write(f"<p style = 'font-size: 18px;'>🍷 {desc}\n\n</p>", unsafe_allow_html=True)
            #st.write(f"  {'''<p style = 'font-size: 18px;'>'''+descriptions[i][3]+'''</p>'''}", unsafe_allow_html=True)

    animated_map(recommendations)
