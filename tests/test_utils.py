"""
Unit tests for utility functions

Testing the helper functions in utils.py to ensure they work correctly
with different types of input data.

Author: Mohsina Zaman Mim
Date: February 9, 2026
"""

import pandas as pd
import pytest
from utils import clean_numeric_column, get_aqi_category, get_aqi_color

def test_clean_numeric_column_basic():
    """Test that commas are removed from numbers"""
    data = pd.Series(["1,234.5", "567", "89.2"])
    result = clean_numeric_column(data)
    
    assert result[0] == 1234.5
    assert result[1] == 567.0
    assert result[2] == 89.2

def test_clean_numeric_column_with_spaces():
    """Test that whitespace is handled properly"""
    data = pd.Series([" 100 ", "  200.5", "300  "])
    result = clean_numeric_column(data)
    
    assert result[0] == 100.0
    assert result[1] == 200.5
    assert result[2] == 300.0

def test_clean_numeric_column_invalid_data():
    """Check that invalid values become NaN"""
    data = pd.Series(["abc", "123", "xyz"])
    result = clean_numeric_column(data)
    
    assert pd.isna(result[0])
    assert result[1] == 123.0
    assert pd.isna(result[2])

def test_aqi_categories():
    """Make sure AQI values map to the right categories"""
    assert get_aqi_category(45) == "Good"
    assert get_aqi_category(95) == "Satisfactory"
    assert get_aqi_category(175) == "Moderate"
    assert get_aqi_category(250) == "Poor"
    assert get_aqi_category(350) == "Very Poor"
    assert get_aqi_category(450) == "Severe"

def test_aqi_category_edge_cases():
    """Test the exact boundary values"""
    assert get_aqi_category(50) == "Good"
    assert get_aqi_category(51) == "Satisfactory"
    assert get_aqi_category(100) == "Satisfactory"
    assert get_aqi_category(101) == "Moderate"

def test_aqi_colors():
    """Verify correct colors are returned for different AQI levels"""
    assert get_aqi_color(30) == "#00FF00"  # Good = Green
    assert get_aqi_color(250) == "#FF9800"  # Poor = Orange
    assert get_aqi_color(500) == "#8B0000"  # Severe = Dark Red