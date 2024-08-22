from sklearn.preprocessing import MinMaxScaler
import pandas as pd


def add_feature(dataset, new_feature_name = 'new_feature', positive_features = [], negative_features = [], preprocessed_features = [], total_count = False):
    """
    Adds a new feature to a DataFrame by normalizing specified features and calculating either the total or mean value.

    Parameters:
    - dataset (pd.DataFrame): The input DataFrame containing the features to be processed.
    - new_feature_name (str, optional): The name of the new feature to be created. Default is 'new_feature'.
    - positive_features (list of str, optional): List of feature names to be treated as positive, which will be normalized directly. Default is an empty list.
    - negative_features (list of str, optional): List of feature names to be treated as negative, which will be reversed before normalization. Default is an empty list.
    - preprocessed_features (list of str, optional): List of feature names to include in the output without normalization. Default is an empty list.
    - total_count (bool, optional): If True, the new feature will be the sum of the normalized features. 
    If False, it will be the mean of the normalized features. Default is False.

    Returns:
    - pd.Series: A Series containing the new feature with the specified name.
    """
    scaler = MinMaxScaler()
    
    #Reverse the values, so that less is good and more is bad
    for column in negative_features:
        data_copy[column] = data_copy[column].max() - data_copy[column]
    
    
    features_to_normalize = positive_features + negative_features
    data_copy = dataset[features_to_normalize].copy()
    data_copy[features_to_normalize] = scaler.fit_transform(data_copy[features_to_normalize])
    if preprocessed_features != []:
        data_copy[preprocessed_features] = dataset[preprocessed_features]
    
    if total_count:
        data_copy[new_feature_name] = data_copy.sum(axis = 1)
    else:
        data_copy[new_feature_name] = data_copy.mean(axis = 1)
    
    return data_copy[new_feature_name]


def normalize_bmi(bmi, upper_bound, lower_bound, max_value, min_value):
    """
    Normalizes a BMI (Body Mass Index) value based on specified bounds and range.

    The function normalizes the BMI value such that it ranges from 0 to 1, where a BMI outside the specified bounds is linearly scaled according to its distance from the bounds.
    A BMI value within the bounds is normalized to 1.

    Parameters:
    - bmi (float): The BMI value to be normalized.
    - upper_bound (float): The upper bound of the BMI range. Values above this bound are linearly scaled.
    - lower_bound (float): The lower bound of the BMI range. Values below this bound are linearly scaled.
    - max_value (float): The maximum possible BMI value used to scale values above the upper bound.
    - min_value (float): The minimum possible BMI value used to scale values below the lower bound.

    Returns:
    - float: The normalized BMI value, which ranges from 0 to 1.
    """
    if bmi > upper_bound:
        distance = (bmi - upper_bound) / (max_value - upper_bound)
    elif bmi < lower_bound:
        distance = (bmi - lower_bound) / (min_value - lower_bound)
    else:
        distance = 0
        
    normalized_value = 1 - distance
    return normalized_value