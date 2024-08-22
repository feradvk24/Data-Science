import pytest
import sys
import os
import pandas as pd
sys.path.append(os.path.abspath('../src'))
from data_manipulation import add_feature, normalize_bmi

def test_normalize_bmi():
    assert abs(normalize_bmi(25, 22, 18, 30, 15) - 0.3333333333333333) < 1e-6
    assert abs(normalize_bmi(16, 22, 18, 30, 15) - 0.2) < 1e-6
    assert abs(normalize_bmi(20, 22, 18, 30, 15) - 1.0) < 1e-6
    assert abs(normalize_bmi(22, 22, 18, 30, 15) - 1.0) < 1e-6
    assert abs(normalize_bmi(18, 22, 18, 30, 15) - 1.0) < 1e-6
    assert abs(normalize_bmi(30, 22, 18, 30, 15) - 0.0) < 1e-6
    assert abs(normalize_bmi(15, 22, 18, 30, 15) - 1.0) < 1e-6
    assert abs(normalize_bmi(22.1, 22, 21.9, 25, 15) - 0.96) < 1e-6
    
    with pytest.raises(ZeroDivisionError):
        normalize_bmi(10, 15, 30, 25, 10)
        

def test_add_feature():
    # Sample data
    data = pd.DataFrame({
        'feature1': [1, 2, 3, 4],
        'feature2': [10, 20, 30, 40],
        'feature3': [100, 200, 300, 400],
        'feature4': [5, 6, 7, 8]
    })

    # Test with positive features, negative features, and total_count=True
    result = add_feature(data, new_feature_name='custom_feature', 
                         positive_features=['feature1', 'feature2'],
                         negative_features=['feature3'],
                         preprocessed_features=['feature4'],
                         total_count=True)
    
    expected_result = pd.Series([1.0, 1.0, 1.0, 1.0], name='custom_feature')
    pd.testing.assert_series_equal(result, expected_result)
    
    # Test with mean calculation
    result = add_feature(data, new_feature_name='mean_feature',
                         positive_features=['feature1', 'feature2'],
                         negative_features=['feature3'],
                         preprocessed_features=['feature4'],
                         total_count=False)
    
    expected_result = pd.Series([0.5, 0.5, 0.5, 0.5], name='mean_feature')
    pd.testing.assert_series_equal(result, expected_result)

    # Test if KeyError is raised for missing features
    with pytest.raises(KeyError):
        add_feature(data, new_feature_name='error_feature',
                    positive_features=['missing_feature'],
                    negative_features=[],
                    preprocessed_features=[],
                    total_count=True)