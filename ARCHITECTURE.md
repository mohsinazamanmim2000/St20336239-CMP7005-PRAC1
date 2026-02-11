# System Architecture

## Overview

I designed this dashboard using Streamlit because it's perfect for data science applications - you can build interactive web apps with pure Python, no need to mess with HTML/CSS/JavaScript.

## How Everything Fits Together

### The Big Picture

```
User Upload (CSV/XLSX)
    ↓
Data Processing (utils.py + pandas)
    ↓
Session State Storage
    ↓
Three Main Pages:
    - Data Overview (initial exploration)
    - EDA (visualizations)
    - Prediction (ML model)
```

## Components Breakdown

### 1. Frontend Layer (What Users See)

**app.py**
- This is the landing page
- Just shows welcome message and instructions
- Pretty simple, mostly text

**pages/ folder**
- Streamlit automatically picks up any .py files here and creates sidebar navigation
- Each page is independent but can share data through session state

### 2. Data Layer

**Session State**
- Think of it like a temporary database that lasts for one user session
- When you upload data in "Data Overview", it gets stored here
- Other pages can access it without re-uploading

**utils.py**
- All my helper functions live here
- Things like cleaning messy data, mapping AQI to categories
- Keeps the main page files clean and focused

### 3. Model Layer

**aqi_model.pkl**
- Pre-trained Random Forest model
- I trained this separately (see Model_Development.ipynb)
- Saved with joblib so we can just load and use it
- Takes 12 pollutant values → outputs AQI prediction

## Why I Made These Design Choices

### Why Streamlit instead of Flask/Django?

**Streamlit pros:**
- Write UI with Python (no HTML templates)
- Auto-refresh when code changes
- Built-in widgets for file upload, charts, etc.
- Perfect for data science demos

**Streamlit cons:**
- Not great for complex multi-user apps
- Limited customization compared to full web frameworks
- Can be slow with very large datasets

For this project, Streamlit was the right call because:
- It's a single-user dashboard
- Focused on data visualization
- Needed to build quickly
- Target users are familiar with data analysis tools, not web apps

### Why Session State instead of Database?

Since this is a personal analysis tool (not storing user data long-term), session state works fine:
- No setup required
- Fast access
- Auto-cleans when user closes browser
- No security concerns about storing pollution data

If I was building this for a company, I'd use PostgreSQL or MongoDB.

### Code Organization

I kept it modular:
- **Pages** handle UI and user interactions
- **utils.py** handles data processing logic
- **Model file** is separate from code

This means I can:
- Test functions independently
- Reuse code across pages
- Update the model without touching the UI
- Add new pages easily

## Data Flow Example

Here's what happens when you predict AQI:

1. User enters pollutant values in `3_Prediction.py`
2. Values get converted to DataFrame (one row)
3. Model loads from `aqi_model.pkl` using joblib
4. Model predicts AQI value
5. My code maps number to category (Good/Poor/etc.)
6. Result displays with color coding and health advice

## Security Considerations

Since this runs locally:
- No user authentication needed
- No database to secure
- File uploads are temporary (don't persist)
- Model file is read-only

If deploying publicly, I'd need to add:
- Input validation (prevent injection attacks)
- Rate limiting (prevent spam)
- HTTPS (encrypt data in transit)
- User authentication (if storing personal data)

## Performance Notes

Current setup handles:
- Files up to ~50MB comfortably
- Datasets with thousands of rows
- Multiple charts without lag

Potential bottlenecks:
- Correlation heatmap can be slow with 20+ columns
- Time-series plots with 100k+ points lag
- Model prediction is fast (<100ms) so not a concern

## Future Architecture Improvements

If I had more time, I'd add:

1. **Database Layer**
   - Store historical predictions
   - Cache processed data
   - Track usage analytics

2. **API Layer**
   - REST API for model predictions
   - Could be used by mobile apps
   - Separate frontend and backend

3. **Background Jobs**
   - Auto-fetch latest air quality data
   - Retrain model monthly
   - Generate weekly reports

4. **Microservices**
   - Separate service for predictions
   - Separate service for visualizations
   - Better scalability

But for an academic project, current architecture is solid - simple, functional, maintainable.

## Conclusion

The architecture is straightforward: upload data → process it → visualize it → predict with it. 

I focused on making it easy to understand and modify rather than over-engineering. Every piece has a clear purpose, and adding new features is pretty simple.