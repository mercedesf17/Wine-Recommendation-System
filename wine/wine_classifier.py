import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_mic_recorder import mic_recorder
import openai
from keys import api_key

client = openai.OpenAI(api_key=api_key)

wine_options = ['red wine', 'white wine', 'rosé wine', 'sparkling wine', 'dessert wine']
flavor_options = ["fruity","spicy", "oaky", "herbal", "chocolate and coffee", "earthy and mineral"]
body_options2 = ["light bodied", "medium bodied", "full bodied"]
sweetness_options2 = ["dry", "balanced", "sweet"]
countries = ["us", "france", "italy", "spain", "portugal", "chile", "argentina", "austria",
        "australia", "germany", "new zealand", "south africa", "israel", "greece", "canada"]
wine_embeddings = wine_options + flavor_options + body_options2 + sweetness_options2 + countries



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

def callback():
    if 'my_recorder_output' in st.session_state:
        audio_bytes = st.session_state.my_recorder_output['bytes']
        if audio_bytes:
            st.audio(audio_bytes, format='audio/mp3')

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

    # Correctly instantiate the mic_recorder component once with all necessary parameters
    mic_recorder(
        key='my_recorder',
        callback=callback,
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,
        use_container_width=False
    )

    prompt = st.chat_input("Please enter your wine preference: Flavors; Aromas; Regions; Sweetness, etc.")
    if prompt:
        st.write(f"Fetching the best wine for you... # {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Given a list of user input characteristics such as wine types, flavors, and countries, map each to the nearest option in our predefined lists, ensuring to strictly adhere to the list for countries. If the user's input includes a country not on our list, like Russia, do not include it in the response. Instead, provide the closest geographical or stylistic relative from the list without defaulting to incorrect or unlisted countries. Use the following lists for mapping: {wine_embeddings}. Return the mapping results in a sentence like 'Based on our database, here is our suggested wine:' followed by the specific characteristics, ensuring country accuracy."
},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150)
        generated_text = response.choices[0].message.content

        st.write(generated_text)






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
