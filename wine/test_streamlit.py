import streamlit as st

import plotly.graph_objects as go

import pandas as pd

from wine.models import *
from wine.dataframing import *


# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'begin'

# Background and style modifications
st.markdown("""
    <style>
        .stApp {
            background-color: #fcb1b9;  /* Pink background color */
        }
        .sidebar .sidebar-content {
            background-color: #fcb1b9;
        }
    </style>
    """, unsafe_allow_html=True)

# Title page
if st.session_state.page == 'begin':
    st.markdown("<h1 style = 'text-align: center; color: black;'> Wine Whisperer</h1>", unsafe_allow_html=True)
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

    # Button to change wine type, wider appearance through column manipulation
    #col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button
    #with col3:
        #if st.button('Change Wine Type', key='change_wine'):
            #st.session_state.page = 'choice'


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
    def plotly_map(X: pd.DataFrame):
        '''Initiates a map of the world with the wines from the input data'''
        fig = go.Figure(go.Scattergeo(lon = X['lon'],
                                    lat = X['lat'],
                                    text = X[['rank', 'region', 'province']],
                                    marker_size = 8,
                                    marker_color = '#c90076'))

        fig.update_geos(projection_type="natural earth",
                    showcountries = True,
                    showsubunits = True,
                    bgcolor = '#fcb1b9',
                    lakecolor = '#fcb1b9',
                    landcolor = '#fcb1b9')

        fig.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

        return fig

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
    st.plotly_chart(plotly_map(recommendations))
