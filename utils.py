"""
Utility Functions for India Air Quality Dashboard

This module contains reusable functions for data processing, validation,
and AQI category mapping used across the application.

Author: Mohsina Zaman Mim
Student ID: St20336239
Date: February 10, 2026
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict


def clean_numeric_column(series: pd.Series) -> pd.Series:
    """
    Clean numeric columns by removing commas and converting to numeric type.
    
    This function handles common data quality issues in air quality datasets:
    - Removes comma separators (e.g., "1,234.5" → 1234.5)
    - Strips leading/trailing whitespace
    - Converts strings to numeric type
    - Handles non-numeric values gracefully (converts to NaN)
    
    Parameters
    ----------
    series : pd.Series
        Input series that may contain comma-separated numbers or strings
        
    Returns
    -------
    pd.Series
        Cleaned series with numeric dtype (float64)
        
    Examples
    --------
    >>> data = pd.Series(["125.5", "1,234", " 89.2 ", "invalid"])
    >>> cleaned = clean_numeric_column(data)
    >>> print(cleaned)
    0     125.5
    1    1234.0
    2      89.2
    3      NaN
    dtype: float64
    
    Notes
    -----
    This function uses errors='coerce' which converts unparseable values
    to NaN instead of raising an exception.
    """
    return pd.to_numeric(
        series.astype(str).str.replace(",", "").str.strip(), 
        errors="coerce"
    )


def get_aqi_category(aqi_value: float) -> str:
    """
    Map AQI numeric value to its categorical classification.
    
    Categories are based on Indian National Air Quality Index (NAQI)
    standards set by the Central Pollution Control Board (CPCB).
    
    Parameters
    ----------
    aqi_value : float
        Numerical AQI value (typically 0-500+)
        
    Returns
    -------
    str
        AQI category name
        
    Examples
    --------
    >>> get_aqi_category(45)
    'Good'
    >>> get_aqi_category(175)
    'Moderate'
    >>> get_aqi_category(425)
    'Severe'
    
    References
    ----------
    - CPCB AQI Guidelines: https://app.cpcbccr.com/ccr_docs/FINAL-REPORT_AQI_.pdf
    """
    if pd.isna(aqi_value):
        return "Unknown"
    elif aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Satisfactory"
    elif aqi_value <= 200:
        return "Moderate"
    elif aqi_value <= 300:
        return "Poor"
    elif aqi_value <= 400:
        return "Very Poor"
    else:
        return "Severe"


def get_aqi_color(aqi_value: float) -> str:
    """
    Get color code for AQI value visualization.
    
    Returns hex color codes that match standard AQI color scheme
    for consistent visualization across the dashboard.
    
    Parameters
    ----------
    aqi_value : float
        Numerical AQI value
        
    Returns
    -------
    str
        Hex color code (e.g., "#00FF00" for green)
        
    Examples
    --------
    >>> get_aqi_color(45)
    '#00FF00'
    >>> get_aqi_color(250)
    '#FF0000'
    """
    if pd.isna(aqi_value):
        return "#808080"  # Gray for unknown
    elif aqi_value <= 50:
        return "#00FF00"  # Green - Good
    elif aqi_value <= 100:
        return "#A8E05F"  # Light Green - Satisfactory
    elif aqi_value <= 200:
        return "#FDD835"  # Yellow - Moderate
    elif aqi_value <= 300:
        return "#FF9800"  # Orange - Poor
    elif aqi_value <= 400:
        return "#FF0000"  # Red - Very Poor
    else:
        return "#8B0000"  # Dark Red - Severe


def get_health_implications(aqi_category: str) -> Dict[str, str]:
    """
    Provide health implications and precautionary measures for each AQI category.
    
    Parameters
    ----------
    aqi_category : str
        AQI category name (e.g., "Good", "Moderate", "Severe")
        
    Returns
    -------
    dict
        Dictionary with keys 'impact' and 'precautions'
        
    Examples
    --------
    >>> info = get_health_implications("Poor")
    >>> print(info['impact'])
    'Breathing discomfort for most people on prolonged exposure'
    """
    implications = {
        "Good": {
            "impact": "Minimal impact",
            "precautions": "None needed. Ideal for outdoor activities."
        },
        "Satisfactory": {
            "impact": "Minor breathing discomfort for sensitive individuals",
            "precautions": "Sensitive groups (children, elderly, asthmatics) should consider reducing outdoor exertion."
        },
        "Moderate": {
            "impact": "Breathing discomfort for people with respiratory diseases",
            "precautions": "Avoid prolonged outdoor activities. Close windows and use air purifiers indoors."
        },
        "Poor": {
            "impact": "Breathing discomfort for most people on prolonged exposure",
            "precautions": "Wear N95 masks outdoors. Limit outdoor activities, especially for children and elderly."
        },
        "Very Poor": {
            "impact": "Respiratory illness on prolonged exposure",
            "precautions": "Avoid all outdoor activities. Keep windows closed. Use indoor air purifiers."
        },
        "Severe": {
            "impact": "Health alert - everyone may experience serious health effects",
            "precautions": "Emergency conditions. Avoid all outdoor exposure. Seek medical attention if experiencing symptoms."
        },
        "Unknown": {
            "impact": "Unable to determine",
            "precautions": "Insufficient data to provide recommendations."
        }
    }
    
    return implications.get(aqi_category, implications["Unknown"])


def validate_pollutant_values(pollutant_dict: Dict[str, float]) -> Dict[str, str]:
    """
    Validate pollutant input values for prediction.
    
    Checks if values are within reasonable ranges based on typical
    air quality measurements. Does not reject values, but warns about
    unusual readings.
    
    Parameters
    ----------
    pollutant_dict : dict
        Dictionary mapping pollutant names to their values
        
    Returns
    -------
    dict
        Dictionary with pollutant names as keys and validation messages as values
        Empty dict if all values are reasonable
        
    Examples
    --------
    >>> values = {'PM2.5': 1500, 'NO2': 75, 'CO': -5}
    >>> warnings = validate_pollutant_values(values)
    >>> print(warnings['PM2.5'])
    'Warning: Unusually high value (>500 μg/m³)'
    """
    warnings = {}
    
    # Define reasonable ranges (min, max) for each pollutant
    # Based on typical measurement ranges in India
    ranges = {
        'PM2.5': (0, 500),
        'PM10': (0, 600),
        'NO': (0, 200),
        'NO2': (0, 200),
        'NOx': (0, 300),
        'NH3': (0, 200),
        'CO': (0, 10),  # mg/m³
        'SO2': (0, 100),
        'O3': (0, 300),
        'Benzene': (0, 50),
        'Toluene': (0, 100),
        'Xylene': (0, 100)
    }
    
    for pollutant, value in pollutant_dict.items():
        if pollutant in ranges:
            min_val, max_val = ranges[pollutant]
            
            if value < 0:
                warnings[pollutant] = f"Warning: Negative value (should be ≥ 0)"
            elif value < min_val:
                warnings[pollutant] = f"Warning: Unusually low value (<{min_val})"
            elif value > max_val:
                warnings[pollutant] = f"Warning: Unusually high value (>{max_val})"
    
    return warnings


def get_pollutant_info(pollutant_name: str) -> Dict[str, str]:
    """
    Provide information about a specific pollutant.
    
    Parameters
    ----------
    pollutant_name : str
        Name of the pollutant (e.g., 'PM2.5', 'NO2', 'O3')
        
    Returns
    -------
    dict
        Dictionary with pollutant information including:
        - full_name: Complete chemical name
        - sources: Primary emission sources
        - health_effects: Key health impacts
        - unit: Measurement unit
        
    Examples
    --------
    >>> info = get_pollutant_info('PM2.5')
    >>> print(info['full_name'])
    'Particulate Matter 2.5'
    """
    pollutant_database = {
        'PM2.5': {
            'full_name': 'Particulate Matter 2.5',
            'sources': 'Vehicle emissions, industrial processes, construction, road dust',
            'health_effects': 'Respiratory diseases, cardiovascular diseases, reduced lung function',
            'unit': 'μg/m³'
        },
        'PM10': {
            'full_name': 'Particulate Matter 10',
            'sources': 'Dust, pollen, mold, vehicle emissions',
            'health_effects': 'Respiratory irritation, asthma aggravation',
            'unit': 'μg/m³'
        },
        'NO': {
            'full_name': 'Nitric Oxide',
            'sources': 'Vehicle combustion, power plants',
            'health_effects': 'Respiratory irritation at high concentrations',
            'unit': 'μg/m³'
        },
        'NO2': {
            'full_name': 'Nitrogen Dioxide',
            'sources': 'Vehicle emissions, power generation',
            'health_effects': 'Lung irritation, reduced immunity to lung infections',
            'unit': 'μg/m³'
        },
        'NOx': {
            'full_name': 'Nitrogen Oxides',
            'sources': 'Combustion processes (vehicles, industry)',
            'health_effects': 'Respiratory tract irritation, acid rain formation',
            'unit': 'μg/m³'
        },
        'NH3': {
            'full_name': 'Ammonia',
            'sources': 'Agricultural activities, animal waste, fertilizers',
            'health_effects': 'Eye and respiratory tract irritation',
            'unit': 'μg/m³'
        },
        'CO': {
            'full_name': 'Carbon Monoxide',
            'sources': 'Incomplete combustion (vehicles, industrial processes)',
            'health_effects': 'Reduces oxygen delivery to organs, can be fatal at high concentrations',
            'unit': 'mg/m³'
        },
        'SO2': {
            'full_name': 'Sulfur Dioxide',
            'sources': 'Coal combustion, industrial processes, volcanoes',
            'health_effects': 'Respiratory problems, aggravates asthma',
            'unit': 'μg/m³'
        },
        'O3': {
            'full_name': 'Ozone',
            'sources': 'Secondary pollutant formed from NOx and VOCs in sunlight',
            'health_effects': 'Respiratory irritation, reduced lung function, aggravates asthma',
            'unit': 'μg/m³'
        },
        'Benzene': {
            'full_name': 'Benzene',
            'sources': 'Vehicle emissions, industrial processes, tobacco smoke',
            'health_effects': 'Cancer (leukemia), blood disorders',
            'unit': 'μg/m³'
        },
        'Toluene': {
            'full_name': 'Toluene',
            'sources': 'Vehicle emissions, paint, solvents',
            'health_effects': 'Central nervous system effects, reproductive effects',
            'unit': 'μg/m³'
        },
        'Xylene': {
            'full_name': 'Xylene',
            'sources': 'Vehicle emissions, paint, varnishes',
            'health_effects': 'Neurological effects, respiratory irritation',
            'unit': 'μg/m³'
        }
    }
    
    return pollutant_database.get(pollutant_name, {
        'full_name': pollutant_name,
        'sources': 'Information not available',
        'health_effects': 'Information not available',
        'unit': 'N/A'
    })


def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Format numbers for display with proper decimal places.
    
    Parameters
    ----------
    value : float
        Number to format
    decimal_places : int, optional
        Number of decimal places (default is 2)
        
    Returns
    -------
    str
        Formatted number string
        
    Examples
    --------
    >>> format_number(123.456789)
    '123.46'
    >>> format_number(0.001, decimal_places=4)
    '0.0010'
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimal_places}f}"


# Constants for the application
FEATURE_COLUMNS = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 
                   'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']

NUMERIC_COLUMNS = FEATURE_COLUMNS + ['AQI']

AQI_THRESHOLDS = {
    'Good': 50,
    'Satisfactory': 100,
    'Moderate': 200,
    'Poor': 300,
    'Very Poor': 400,
    'Severe': float('inf')
}