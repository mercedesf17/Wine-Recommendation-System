import pandas as pd

from sklearn.neighbors import KNeighborsRegressor

# Importing the wine data
df = pd.read_csv('data/final_dataframe.csv')

def filtered_rows(prince_range: tuple,
                wine_type: str) -> pd.DataFrame:
    '''Returns the rows that match the price range and wine type'''
    filtered = df[df['price'].between(prince_range[0], prince_range[1]) & (df['wine_type'] == wine_type)]

    return filtered

def train_model(X: pd.DataFrame):
    model = KNeighborsRegressor(n_neighbors = 30)

    features = ['dry_wine', 'sweet_wine', 'fruity_aroma', 'spicy_aroma',
                'herb_aroma', 'oak_aroma', 'chocolate_aroma', 'floral_aroma',
                'body_light', 'body_medium', 'body_full', 'encoded_country']

    X_features = X[features]
    y = pd.Series(X_features.index)

    model.fit(X_features, y)

    return model

def neighbors(model,
              filtered: pd.DataFrame,
              X: pd.DataFrame) -> pd.DataFrame:
    '''Returns the 15 nearest neighbors to the input data'''
    # Question: Do we want to add the cosine similarity?

    neighbors = model.kneighbors(X, n_neighbors = 5, return_distance = False)

    indices = neighbors[0].tolist()

    return filtered.iloc[indices]

def describe(X: pd.DataFrame) -> list:
    '''Returns the decriptions of the wines from the input data'''
    descriptions = []

    for i in range(len(X)):
        #line_1 = f'Recommendation {i+1}: \n'
        line_2 = f"{X.iloc[i]['title']}\n"
        line_3 = f"Price: ${X.iloc[i]['price']}\n"
        line_4 = (f'''This wine is a {X.iloc[i]['variety']} from
                             {X.iloc[i]['province']}, {X.iloc[i]['country']}\n''')
        line_5 = X.iloc[i]['description']+'\n'+('_'*150)

        descriptions.append([line_2, line_3, line_4, line_5])

    return descriptions
