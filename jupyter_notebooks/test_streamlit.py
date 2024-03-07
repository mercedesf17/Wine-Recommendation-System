import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

# Load your DataFrame
df = pd.read_csv('expanded_dataframe.csv')  # Replace with the path to your dataset

# Train your KNN model
X = df[['dry_wine', 'sweet_wine', 'fruity_aroma', 'spicy_aroma', 'herb_aroma', 'oak_aroma', 'chocolate_aroma', 'floral_aroma', 'body_light', 'body_medium', 'body_full']]
y = df['index']
neigh = KNeighborsRegressor(n_neighbors=10)
neigh.fit(X, y)

# Streamlit app
st.title("Wine Prediction App")

# User input
st.sidebar.header("User Input")
dry_or_sweet = st.sidebar.radio("Select Wine Type", ['Dry Wine', 'Sweet Wine'])
aromas = st.sidebar.multiselect("Select Aromas", ['fruity_aroma', 'spicy_aroma', 'herb_aroma', 'oak_aroma', 'chocolate_aroma', 'floral_aroma'])
body = st.sidebar.radio("Select Body", ['body_light', 'body_medium', 'body_full'])

# Map user input to binary features
input_features = {
    'dry_wine': 1 if dry_or_sweet == 'Dry Wine' else 0,
    'sweet_wine': 1 if dry_or_sweet == 'Sweet Wine' else 0,
}
for aroma in aromas:
    input_features[aroma] = 1
for b in ['body_light', 'body_medium', 'body_full']:
    input_features[b] = 1 if b == body else 0

# Make prediction
input_data = pd.DataFrame([input_features])
prediction = neigh.predict(input_data)[0]

# Display prediction
st.subheader("Prediction")
st.write(f"The predicted wine index is: {prediction}")
