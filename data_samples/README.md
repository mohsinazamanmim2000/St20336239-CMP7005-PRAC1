# Sample Data Files

These are test datasets I created to help demonstrate the dashboard functionality and make testing easier.

## Files Included

### 1. test_minimal.csv
Basic sample with just a few rows - good for quick testing
- 3 cities (Delhi, Mumbai, Kolkata)
- All required pollutant columns
- No missing values

### 2. test_missing.csv
Contains some missing values to test how the app handles incomplete data
- Same structure as test_minimal
- Some pollutant values are blank to simulate real-world data issues

### 3. test_timeseries.csv
Includes date column for testing the time-series visualizations
- One week of data for Delhi
- Shows how pollution changes over time

## How to Use

1. Go to the "Data Overview" page
2. Click "Browse files"
3. Upload any of these test files
4. Navigate to other pages to see the visualizations

## Data Format

All files follow this structure:
```
Date, City, PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene, AQI
```

The units are:
- PM2.5, PM10: μg/m³
- Gases (NO, NO2, etc.): μg/m³
- CO: mg/m³
- AQI: Index value (0-500+)

## Notes

These are simplified datasets for testing purposes. Real air quality data would have:
- More records (thousands of rows)
- Additional metadata
- Hourly measurements instead of daily
- Station information

But these samples are perfect for demonstrating the dashboard features without overwhelming the system.