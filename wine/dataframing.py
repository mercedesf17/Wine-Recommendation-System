import pandas as pd

'''This file gives the initial blank dataframe for the recommendation model.
It also has functions to update the dataframe with the users input from streamlit'''

# Initial dictionary for the features, all blank
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

def update_dryness(dryness_selected: str = None,
                   features_dict: dict = features_dict):
    '''Updates the dryness values in the features dictionary'''
    if dryness_selected == 'Sweet':
        features_dict['sweet_wine'] = 1
    if dryness_selected == 'Dry':
        features_dict['dry_wine'] = 1

    return features_dict

def update_aromas(tastes_aromas_selected: list,
                  features_dict: dict = features_dict):
    '''Updates the aroma values in the features dictionary'''
    aroma_features = ['fruity_aroma', 'spicy_aroma', 'oak_aroma', 'herb_aroma', 'chocolate_aroma', 'floral_aroma']

    for aroma in tastes_aromas_selected:
        features_dict[aroma_features[tastes_aromas_selected.index(aroma)]] = 1

    return features_dict

def update_body(body_selected: list,
                features_dict: dict = features_dict):
    '''Updates the body values in the features dictionary'''
    body_features = {'Light': 'body_light',
                     'Medium': 'body_medium',
                     'Full': 'body_full'}

    for body in body_selected:
        features_dict[body_features[body]] = 1

    return features_dict

def update_country(selected_country: str,
                   features_dict: dict = features_dict):
    '''Updates the country values in the features dictionary'''
        # Mapping selected country to corresponding value in the dataset
    country_dict = {'Portugal': 1, 'Spain': 2, 'France': 3, 'Germany': 4, 'Austria': 5,
                    'Italy': 6, 'Greece': 7, 'Israel': 8, 'South Africa': 9, 'Australia': 10,
                    'New Zealand': 11, 'Chile': 12, 'Argentina': 13, 'US': 14, 'Canada': 15}

    features_dict['encoded_country'] = country_dict[selected_country]

    return features_dict
