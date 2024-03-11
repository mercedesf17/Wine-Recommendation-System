import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Initialize session state for navigation and wine type selection
if 'page' not in st.session_state:
    st.session_state.page = 'choice'
if 'wine_type' not in st.session_state:
    st.session_state.wine_type = 'Red Wine'  # Default selection to ensure radio button has a default value

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
.content-area, .block-container {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
    color: white; /* Adjust text color to improve readability */
    padding: 20px; /* Some padding for aesthetics */
    border-radius: 10px; /* Optional: rounded corners for the box */
}
</style>
""", unsafe_allow_html=True)

# Define regions with their corresponding countries


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

    if st.button('Show Options'):
        st.session_state.page = 'details'



elif st.session_state.page == 'details':
    st.markdown(f"## **You've selected {st.session_state.wine_type}**!")

    # Tastes/aromas and textures and countries options
    regions = {
    "Europe": ["France", "Germany", "Portugal", "Spain", "Italy", "Greece", "Austria"],
    "South America": ["Argentina", "Chile"],
    "Oceania": ["Australia", "New Zealand"],
    "North America": ["US", "Canada"],
}
    body_options = ["Light Bodied", "Medium Bodied", "Full Bodied"]
    sweetness_options = ["Dry", "Balanced", "Sweet"]
    tastes_aromas_options = ["Fruity", "Spicy", "Oaky", "Herbal", "Earthy and Mineral", "Chocolate and Coffee" ]

    selected_body_options = []
    selected_sweetness_options = []
    selected_tastes_aromas = []

    # Split selected body options
    st.markdown("#Select the preferable wine Body, Sweetness, Flavor Profiles")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.checkbox(body_options[0], key=f"bo_{body_options[0]}"):
            selected_body_options.append(body_options[0])

    with col2:
        if st.checkbox(body_options[1], key=f"bo_{body_options[1]}"):
            selected_body_options.append(body_options[1])

    with col3:
        if st.checkbox(body_options[2], key=f"bo_{body_options[2]}"):
            selected_body_options.append(body_options[2])

    # Display selected body options
    if selected_body_options:
        st.write(f'You chose {" and ".join(selected_body_options)} bodies!')
    else:
        st.write('You have not selected any body yet')

    # Split selected sweetness options
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.checkbox(sweetness_options[0], key=f"bo_{sweetness_options[0]}"):
            selected_sweetness_options.append(sweetness_options[0])

    with col2:
        if st.checkbox(sweetness_options[1], key=f"bo_{sweetness_options[1]}"):
            selected_sweetness_options.append(body_options[1])

    with col3:
        if st.checkbox(sweetness_options[2], key=f"bo_{sweetness_options[2]}"):
            selected_sweetness_options.append(sweetness_options[2])

    # Display selected sweetness options
    if selected_sweetness_options:
        st.write(f'You chose {" and ".join(selected_body_options)} sweetness option!')
    else:
        st.write('You have not selected any sweetness yet')

    # Split tastes/aromas into two columns
    col1, col2 = st.columns(2)

    with col1:
        for option in tastes_aromas_options[:len(tastes_aromas_options)//2]:
            if st.checkbox(option, key=f"ta_{option}"):
                selected_tastes_aromas.append(option)

    with col2:
        for option in tastes_aromas_options[len(tastes_aromas_options)//2:]:
            if st.checkbox(option, key=f"ta_{option}"):
                selected_tastes_aromas.append(option)

    # Display selected tastes/aromas
    if selected_tastes_aromas:
        st.write(f'You chose {" and ".join(selected_tastes_aromas)} taste profiles!')
    else:
        st.write('You have not selected any taste profile yet')

    st.markdown("### Select Regions and Countries and Price Range:")
    for region, countries in regions.items():
    # Create a checkbox for each region
        if st.checkbox(region, key=f"region_{region}"):
        # If the region is selected, display checkboxes for its countries
            for country in countries:
                # Use st.columns to indent the country checkboxes
                col1, col2 = st.columns([1, 10])  # Adjust as needed for better indentation
                with col2:
                    st.checkbox(country, key=f"country_{country}")

    st.write("Select Your Price Range:")
    price_range = st.slider("Price Range ($)", 0, 200, (10, 100))
    st.markdown(f"<p style='font-family: sans-serif; font-size: 16px;'>Your selected price range: $ {price_range[0]} - ${price_range[1]}</p>", unsafe_allow_html=True)

    # Change Wine Type button

    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button('Change Wine Type', key='change_wine'):
            st.session_state.page = 'choice'

    # Map visualization
    file_path = "../data/latlon_wine_data.csv"
    latlon_df = pd.read_csv(file_path)
    fig = go.Figure(go.Scattergeo(lon=latlon_df['lon'], lat=latlon_df['lat'], text=latlon_df['address']))
    fig.update_geos(projection_type="natural earth", showcountries=True, showsubunits=True, bgcolor='#1e1e1e', lakecolor='#1e1e1e')
    fig.update_layout(height=400, margin={"r": 0, "t": 0, "l": 0, "b": 0}, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
    st.plotly_chart(fig)
