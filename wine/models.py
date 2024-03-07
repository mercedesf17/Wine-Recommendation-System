import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsRegressor

df = pd.read_csv('../data/final_dataframe.csv')

def neighbors(model, X: pd.DataFrame):
    '''Returns the 15 nearest neighbors to the input data'''
    # Question: Do we want to add the cosine similarity?

    neighbors = model.kneighbors(X, n_neighbors = 15, return_distance = True)

    indices = neighbors[1][0].tolist()

    return df.iloc[indices]

def match_type(X: pd.DataFrame):
    '''Returns the nearest neighbors whose wine type matches the inpute data'''
    wine_type = X['wine_type']

    neighbors = neighbors(X)

    filtered_neighbors = neighbors[neighbors['wine_type'] == wine_type]

    if len(filtered_neighbors) > 5:
        return filtered_neighbors.iloc[:5]

    return filtered_neighbors

def describe(X: pd.DataFrame):
    '''Returns the decriptions of the wines from the input data'''
    for i in range(len(X)):
        print(f'Recommendation number {i+1}:\n')
        print(f'''This wine is a {X.iloc[i]['wine_type']} wine from
              {X.iloc[i]['province']}, {X.iloc[i]['country']}''')
        print(X.iloc[i]['description'])
        print('_'*150)

# Train model and save it as a pickle file
# When we want to use the model we can just load it from the pickle file
# That way we don't need to load and train model every time we want to use it
# And here we just keep neighbors() and match_type() and describe()
