import streamlit as st

import plotly.graph_objects as go

import pandas as pd

from wine.models import *


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

    #if st.button('Show Aromas and Countries'):
        #st.session_state.page = 'details'

elif st.session_state.page == 'details':
    st.markdown(f"## **You selected {st.session_state.wine_type}**!")
    #button_key = f'get_recommendations_{time.time()}'
    #col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button
    #with col3:
        #if st.button('Get Recommendations', key=button_key):
            #st.session_state.page = 'choice'
            #pass

    # Dryness selection in two parallel columns
st.write("Select Preferred Dryness:")
dryness_options = ['Sweet', 'Dry']
col1, col2 = st.columns(2)  # Create two columns
dryness_selected = []

    # Distribute checkboxes across two columns
for i, option in enumerate(dryness_options):
    if i % 2 == 0:
        with col1:
            if st.checkbox(option, key=option + "1"):
                dryness_selected.append(option)
    else:
        with col2:
            if st.checkbox(option, key=option + "2"):
                dryness_selected.append(option)

if dryness_selected:
    st.write("You selected:", ", ".join(dryness_selected))
else:
    st.write("No dryness selected")

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

st.write("Select Preferred Body :")
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
    st.write("No textures selected")

    # Price range slider
st.write("Select Your Price Range:")
price_range = st.slider("Price Range ($)", 0, 200, (10, 100))
st.write(f"Your selected price range: ${price_range[0]} - ${price_range[1]}")

    # Country selector
countries = ["Portugal", "Spain", "France", "Germany", "Austria",
             "Italy", "Greece", "Israel", "South Africa", "Australia",
             "New Zealand", "Chile", "Argentina", "US", "Canada"]
selected_country = st.selectbox("Select Country:", countries)
st.write(f"You selected: {selected_country}")

    # Button to change wine type, wider appearance through column manipulation
    #col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button
    #with col3:
        #if st.button('Change Wine Type', key='change_wine'):
            #st.session_state.page = 'choice'

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
                 'body_full': 0}


# Mapping selected country to corresponding value in the dataset
country_dict = {'Portugal': 1, 'Spain': 2, 'France': 3, 'Germany': 4, 'Austria': 5,
                'Italy': 6, 'Greece': 7, 'Israel': 8, 'South Africa': 9, 'Australia': 10,
                'New Zealand': 11, 'Chile': 12, 'Argentina': 13, 'US': 14, 'Canada': 15}
features_dict['encoded_country'] = country_dict[selected_country]

# Mapping wine types to the corresponding values in the dataset
wine_type = st.session_state.wine_type if 'wine_type' in st.session_state else 'Red Wine'
wine_dict = {'Red Wine': 'red',
             'White Wine': 'white',
             'Rosé Wine': 'rose',
             'Sparkling Wine': 'sparkling',
             'Dessert Wine': 'dessert'}
wine_type_new =  wine_dict.get(wine_type, 'red')
#features_dict['wine_type'] = wine_type_new

# Changing aroma values to 1 if they appear in tastes_aromas_selected
aroma_features = ['fruity_aroma', 'spicy_aroma', 'oak_aroma', 'herb_aroma', 'chocolate_aroma', 'floral_aroma']

for aroma in tastes_aromas_selected:
    features_dict[aroma_features[tastes_aromas_selected.index(aroma)]] = 1

# Changing the body values to 1 if they appear in body_selected
body_features = ["body_light", "body_medium", "body_full"]

for body in body_selected:
    features_dict[body_features[body_selected.index(body)]] = 1

col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the middle column width for more space to the left of the button

with col3:

    if st.button('Get Recommendations', key='get_recommendations'):
    # Creating a DataFrame for the input features
        X_test = pd.DataFrame(features_dict, index=[0])

    # Initiating and training the model
        filtered = filtered_rows(price_range, wine_type_new)
        model = train_model(filtered)

    # Get the recommended wines by calling the match_type and describe functions from models
        recommendations = neighbors(model, filtered, X_test)
        recommendations['rank'] = range(1, len(recommendations) + 1)
        descriptions = describe(recommendations)

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
                bgcolor = '#FF69B4',
                lakecolor = '#FF69B4',
                landcolor = '#ffacd5')

    fig.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                   'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

    return fig

# Display the recommendations
st.write("Recommended Wines:")
st.write('\n'.join(descriptions))
st.plotly_chart(plotly_map(recommendations))

##PROBLEMS
# model.pkl does not take price as a feature; not sure what to do for range of prices
# filtering by country is not ideal; maybe different models for different continents? ruh roh
