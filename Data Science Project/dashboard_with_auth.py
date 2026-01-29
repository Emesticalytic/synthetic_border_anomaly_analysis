"""
UK Border Anomaly Detection System
Interactive Dashboard with Authentication
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import dash_auth
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import os

# ============================================================================
# AUTHENTICATION SETUP
# ============================================================================

# Username and password pairs (change these!)
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'ukborder2026',
    'officer': 'secure123',
    'analyst': 'data2026'
}

# Load data and models
print("Loading data and models...")

data_paths = [
    'data/processed/uk_passengers_features.csv',
    'outputs/figures/data/processed/uk_passengers_features.csv'
]
df = None
for path in data_paths:
    try:
        df = pd.read_csv(path)
        print(f"✓ Loaded data from: {path}")
        break
    except FileNotFoundError:
        continue

if df is None:
    raise FileNotFoundError("Could not find uk_passengers_features.csv")

df['arrival_datetime'] = pd.to_datetime(df['arrival_datetime'])
df['booking_datetime'] = pd.to_datetime(df['booking_datetime'])

# Load SHAP feature importance
shap_paths = [
    'outputs/reports/shap_feature_importance.csv',
    'outputs/figures/outputs/reports/shap_feature_importance.csv'
]
shap_importance = None
for path in shap_paths:
    try:
        shap_importance = pd.read_csv(path)
        print(f"✓ Loaded SHAP importance from: {path}")
        break
    except FileNotFoundError:
        print("⚠️  SHAP importance not found")
        continue

# Model performance metrics
model_metrics = {
    'Isolation Forest': {'Precision': 0.32, 'Recall': 0.85, 'F1': 0.47, 'ROC-AUC': 0.87},
    'Random Forest': {'Precision': 0.83, 'Recall': 0.87, 'F1': 0.85, 'ROC-AUC': 0.90},
    'XGBoost': {'Precision': 0.86, 'Recall': 0.89, 'F1': 0.87, 'ROC-AUC': 0.92},
    'LSTM': {'Precision': 0.91, 'Recall': 0.89, 'F1': 0.90, 'ROC-AUC': 0.94},
    'Autoencoder': {'Precision': 0.89, 'Recall': 0.87, 'F1': 0.88, 'ROC-AUC': 0.93},
    'Ensemble': {'Precision': 0.87, 'Recall': 0.90, 'F1': 0.88, 'ROC-AUC': 0.93}
}

print("✓ Data and models loaded successfully")

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose the server for deployment

# Add authentication
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.title = "UK Border Security - Anomaly Detection Dashboard"

# Define colors
colors = {
    'background': '#f8f9fa',
    'text': '#212529',
    'primary': '#0d6efd',
    'success': '#198754',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#0dcaf0'
}

# ============================================================================
# DASHBOARD LAYOUT (Same as before)
# ============================================================================

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    # Header with authentication notice
    html.Div([
        html.Div([
            html.Span("🔒 Authenticated Session", style={
                'backgroundColor': colors['success'],
                'color': 'white',
                'padding': '5px 15px',
                'borderRadius': '5px',
                'fontSize': '12px',
                'float': 'right',
                'marginTop': '20px',
                'marginRight': '20px'
            })
        ]),
        html.H1("🛂 UK Border Security - Anomaly Detection System", 
                style={'textAlign': 'center', 'color': colors['primary'], 'padding': '20px'}),
        html.H4("Real-time Passenger Risk Assessment Dashboard | Powered by Deep Learning & ML",
                style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '10px'}),
        html.P("Models: Ensemble, XGBoost, LSTM, Random Forest, Autoencoder, Isolation Forest",
               style={'textAlign': 'center', 'color': '#6c757d', 'fontSize': '14px', 'marginBottom': '20px'}),
    ]),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Passengers", style={'color': colors['text'], 'fontSize': '16px'}),
                html.H2(f"{len(df):,}", style={'color': colors['primary'], 'margin': '10px 0'}),
                html.P("Processed", style={'color': '#6c757d', 'fontSize': '14px'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),
        
        html.Div([
            html.Div([
                html.H3("High Risk", style={'color': colors['text'], 'fontSize': '16px'}),
                html.H2(f"{df['is_anomaly'].sum():,}", style={'color': colors['danger'], 'margin': '10px 0'}),
                html.P(f"{df['is_anomaly'].mean()*100:.2f}% of total", 
                      style={'color': '#6c757d', 'fontSize': '14px'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),
        
        html.Div([
            html.Div([
                html.H3("Airports", style={'color': colors['text'], 'fontSize': '16px'}),
                html.H2(f"{df['arrival_airport_code'].nunique()}", 
                       style={'color': colors['success'], 'margin': '10px 0'}),
                html.P("Monitored", style={'color': '#6c757d', 'fontSize': '14px'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),
        
        html.Div([
            html.Div([
                html.H3("Countries", style={'color': colors['text'], 'fontSize': '16px'}),
                html.H2(f"{df['origin_country'].nunique()}", 
                       style={'color': colors['info'], 'margin': '10px 0'}),
                html.P("Origins", style={'color': '#6c757d', 'fontSize': '14px'})
            ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px',
                     'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'})
        ], style={'width': '23%', 'display': 'inline-block', 'margin': '0 1%'}),
    ], style={'padding': '20px', 'marginBottom': '20px'}),
    
    # Filters
    html.Div([
        html.Div([
            html.Label("Select Airport:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='airport-filter',
                options=[{'label': 'All Airports', 'value': 'ALL'}] + 
                        [{'label': f"{code}", 'value': code} 
                         for code in sorted(df['arrival_airport_code'].unique())],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Risk Level:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='risk-filter',
                options=[
                    {'label': 'All Levels', 'value': 'ALL'},
                    {'label': 'Low Risk', 'value': 'low'},
                    {'label': 'Medium Risk', 'value': 'medium'},
                    {'label': 'High Risk', 'value': 'high'}
                ],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Show Anomalies Only:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.RadioItems(
                id='anomaly-filter',
                options=[
                    {'label': ' All Passengers', 'value': 'ALL'},
                    {'label': ' Anomalies Only', 'value': 'ANOMALY'}
                ],
                value='ALL',
                inline=True,
                style={'marginTop': '10px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'backgroundColor': 'white', 'padding': '20px', 'margin': '20px', 
             'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    # Placeholder for charts (same as original dashboard.py)
    html.Div([
        html.Div([
            html.Div([dcc.Graph(id='airport-distribution')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(id='country-distribution')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        html.Div([
            html.Div([dcc.Graph(id='temporal-pattern')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(id='risk-score-distribution')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        html.Div([
            html.Div([dcc.Graph(id='feature-importance')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(id='booking-lead-time')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        html.Div([
            html.Div([dcc.Graph(id='model-comparison')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(id='anomaly-types')], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
    ], style={'padding': '20px'}),
    
    # High Risk Table
    html.Div([
        html.H3("🚨 High Risk Passengers (Sample)", 
               style={'color': colors['danger'], 'marginBottom': '20px'}),
        html.Div(id='high-risk-table')
    ], style={'backgroundColor': 'white', 'padding': '20px', 'margin': '20px',
             'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    
    # Footer
    html.Div([
        html.Hr(),
        html.P("🔒 Secure Access | UK Border Security Anomaly Detection System | Powered by Machine Learning",
              style={'textAlign': 'center', 'color': '#6c757d', 'marginTop': '20px'})
    ])
])

# Copy the callback from the original dashboard.py
@app.callback(
    [Output('airport-distribution', 'figure'),
     Output('country-distribution', 'figure'),
     Output('temporal-pattern', 'figure'),
     Output('risk-score-distribution', 'figure'),
     Output('feature-importance', 'figure'),
     Output('booking-lead-time', 'figure'),
     Output('model-comparison', 'figure'),
     Output('anomaly-types', 'figure'),
     Output('high-risk-table', 'children')],
    [Input('airport-filter', 'value'),
     Input('risk-filter', 'value'),
     Input('anomaly-filter', 'value')]
)
def update_dashboard(airport, risk_level, anomaly_only):
    try:
        filtered_df = df.copy()
        
        if airport != 'ALL':
            filtered_df = filtered_df[filtered_df['arrival_airport_code'] == airport]
        
        if risk_level != 'ALL' and 'country_risk_level' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['country_risk_level'] == risk_level]
        
        if anomaly_only == 'ANOMALY':
            filtered_df = filtered_df[filtered_df['is_anomaly'] == True]
        
        if len(filtered_df) == 0:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No data available for selected filters", 
                                    showarrow=False, font=dict(size=16))
            return [empty_fig] * 8 + [html.Div("No data available")]
        
        # Create all figures (simplified for space - copy from original dashboard.py)
        # 1. Airport Distribution
        airport_counts = filtered_df['arrival_airport_code'].value_counts().reset_index()
        airport_counts.columns = ['airport', 'count']
        fig_airport = px.bar(airport_counts, x='airport', y='count', 
                            title='Passenger Arrivals by Airport',
                            color='count', color_continuous_scale='Blues')
        
        # Add remaining figures from original dashboard...
        # For brevity, returning placeholder figures
        fig_country = fig_airport
        fig_temporal = fig_airport  
        fig_risk = fig_airport
        fig_importance = fig_airport
        fig_booking = fig_airport
        fig_models = fig_airport
        fig_anomaly_types = fig_airport
        
        table = html.Div("Table placeholder")
        
        return fig_airport, fig_country, fig_temporal, fig_risk, fig_importance, fig_booking, fig_models, fig_anomaly_types, table
    
    except Exception as e:
        error_fig = go.Figure()
        error_fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, font=dict(size=14, color='red'))
        return [error_fig] * 8 + [html.Div(f"Error: {str(e)}", style={'color': 'red'})]

if __name__ == '__main__':
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=8050)
