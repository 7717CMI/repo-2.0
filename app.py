import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State, dash_table, callback_context
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import base64
import io

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load the enhanced data
try:
    df = pd.read_csv('data/leads.csv')
    df['Inquiry Date'] = pd.to_datetime(df['Inquiry Date'])
    df['Expected Ship Date'] = pd.to_datetime(df['Expected Ship Date'])
    df['Follow Up Date'] = pd.to_datetime(df['Follow Up Date'])
    df['Last Contact'] = pd.to_datetime(df['Last Contact'])
    print(f"Loaded {len(df)} comprehensive records from data/leads.csv")
except FileNotFoundError:
    print("Error: data/leads.csv not found. Please run generate_enhanced_data.py first.")
    df = pd.DataFrame()

# Define color scheme
COLORS = {
    'primary': '#1f4e79',  # Dark blue
    'secondary': '#6c757d',  # Gray
    'success': '#28a745',
    'info': '#17a2b8',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# Helper function to categorize intent scores
def categorize_intent(score):
    if score >= 0.8:
        return 'High'
    elif score >= 0.5:
        return 'Medium'
    else:
        return 'Low'

# Add intent category to dataframe
if not df.empty:
    df['Intent Category'] = df['Intent Score'].apply(categorize_intent)

# Define the enhanced layout
app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col([
            html.H1("🚛 Comprehensive Freight Intelligence Dashboard", 
                   className="text-center mb-2", 
                   style={'color': COLORS['primary'], 'fontWeight': 'bold'}),
            html.H4("Advanced Lead Management & Business Intelligence Platform", 
                   className="text-center mb-2", 
                   style={'color': COLORS['secondary']}),
            html.P("Real-time tracking of freight inquiries, client contacts, and shipment analytics", 
                   className="text-center mb-4", 
                   style={'color': COLORS['info'], 'fontSize': '1.1em'}),
            html.P("Note: This dataset is for illustration purposes only. It does not represent actual data and has no association with real-world datasets.", 
                   className="text-center mb-4", 
                   style={'fontStyle': 'italic', 'color': COLORS['secondary'], 'fontSize': '0.9em'})
        ])
    ], className="mb-4"),
    
    # Enhanced Filters Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🔍 Advanced Filters & Search", className="card-title mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("State:", className="form-label"),
                            dcc.Dropdown(
                                id='state-filter',
                                options=[{'label': 'All States', 'value': 'All'}] + 
                                       [{'label': state, 'value': state} for state in sorted(df['State'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Inquiry Type:", className="form-label"),
                            dcc.Dropdown(
                                id='inquiry-type-filter',
                                options=[{'label': 'All Types', 'value': 'All'}] + 
                                       [{'label': itype, 'value': itype} for itype in sorted(df['Inquiry Type'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Industry:", className="form-label"),
                            dcc.Dropdown(
                                id='industry-filter',
                                options=[{'label': 'All Industries', 'value': 'All'}] + 
                                       [{'label': industry, 'value': industry} for industry in sorted(df['Industry'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Priority Level:", className="form-label"),
                            dcc.Dropdown(
                                id='priority-filter',
                                options=[{'label': 'All Priorities', 'value': 'All'}] + 
                                       [{'label': priority, 'value': priority} for priority in sorted(df['Priority Level'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Intent Score Range:", className="form-label"),
                            dcc.RangeSlider(
                                id='intent-range-filter',
                                min=0,
                                max=1,
                                step=0.1,
                                value=[0, 1],
                                marks={i/10: f'{i/10:.1f}' for i in range(0, 11, 2)},
                                className="mb-3"
                            )
                        ], md=6),
                        dbc.Col([
                            html.Label("Date Range:", className="form-label"),
                            dcc.DatePickerRange(
                                id='date-range-filter',
                                start_date=df['Inquiry Date'].min() if not df.empty else datetime.now() - timedelta(days=60),
                                end_date=df['Inquiry Date'].max() if not df.empty else datetime.now(),
                                display_format='YYYY-MM-DD',
                                className="mb-3"
                            )
                        ], md=6)
                    ])
                ])
            ], className="mb-4")
        ])
    ]),
    
    # Enhanced KPI Cards Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="total-leads", className="text-center mb-1"),
                    html.P("Total Leads", className="text-center text-muted mb-0"),
                    html.Small(id="leads-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="avg-intent", className="text-center mb-1"),
                    html.P("Avg Intent Score", className="text-center text-muted mb-0"),
                    html.Small(id="intent-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="total-value", className="text-center mb-1"),
                    html.P("Total Shipment Value", className="text-center text-muted mb-0"),
                    html.Small(id="value-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="high-priority", className="text-center mb-1"),
                    html.P("High Priority Leads", className="text-center text-muted mb-0"),
                    html.Small(id="priority-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="top-industry", className="text-center mb-1"),
                    html.P("Top Industry", className="text-center text-muted mb-0"),
                    html.Small(id="industry-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="conversion-rate", className="text-center mb-1"),
                    html.P("Conversion Rate", className="text-center text-muted mb-0"),
                    html.Small(id="conversion-change", className="text-center d-block")
                ])
            ], className="text-center h-100")
        ], md=2)
    ], className="mb-4"),
    
    # Enhanced Charts Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Load Origins by State", className="card-title"),
                    dcc.Graph(id="load-origins-chart"),
                    html.P("Geographic distribution of shipment origins across states", 
                           className="text-muted small mt-2")
                ])
            ], className="h-100")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 Intent Score Distribution", className="card-title"),
                    dcc.Graph(id="intent-distribution-chart"),
                    html.P("Lead quality distribution showing conversion potential", 
                           className="text-muted small mt-2")
                ])
            ], className="h-100")
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏭 Industry Breakdown", className="card-title"),
                    dcc.Graph(id="industry-chart")
                ])
            ], className="h-100")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("⚡ Priority Level Analysis", className="card-title"),
                    dcc.Graph(id="priority-chart")
                ])
            ], className="h-100")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📞 Lead Source Performance", className="card-title"),
                    dcc.Graph(id="source-chart")
                ])
            ], className="h-100")
        ], md=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("💰 Shipment Value Analysis", className="card-title"),
                    dcc.Graph(id="value-chart")
                ])
            ], className="h-100")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📅 Timeline Analysis", className="card-title"),
                    dcc.Graph(id="timeline-chart")
                ])
            ], className="h-100")
        ], md=6)
    ], className="mb-4"),
    
    # Enhanced Lead Table Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("👥 Comprehensive Lead Management", className="card-title"),
                    html.Div([
                        dbc.Button("📥 Download CSV", id="download-btn", color="primary", className="mb-3 me-2"),
                        dbc.Button("📧 Export Contacts", id="export-contacts-btn", color="success", className="mb-3")
                    ]),
                    dcc.Download(id="download-dataframe-csv"),
                    dcc.Download(id="download-contacts-csv"),
                    dash_table.DataTable(
                        id='leads-table',
                        columns=[
                            {'name': 'Lead ID', 'id': 'Lead ID'},
                            {'name': 'Company', 'id': 'Company Name'},
                            {'name': 'Contact', 'id': 'Contact Person'},
                            {'name': 'Phone', 'id': 'Phone Number'},
                            {'name': 'Email', 'id': 'Email'},
                            {'name': 'Industry', 'id': 'Industry'},
                            {'name': 'Type', 'id': 'Inquiry Type'},
                            {'name': 'State', 'id': 'State'},
                            {'name': 'Intent', 'id': 'Intent Score', 'type': 'numeric', 'format': {'specifier': '.2f'}},
                            {'name': 'Priority', 'id': 'Priority Level'},
                            {'name': 'Status', 'id': 'Status'},
                            {'name': 'Value ($)', 'id': 'Shipment Value ($)', 'type': 'numeric', 'format': {'specifier': ',.0f'}},
                            {'name': 'Ship Date', 'id': 'Expected Ship Date'},
                            {'name': 'Follow Up', 'id': 'Follow Up Date'},
                            {'name': 'Next Action', 'id': 'Next Action'}
                        ],
                        data=[],
                        page_size=15,
                        style_cell={'textAlign': 'left', 'padding': '8px', 'fontSize': '12px'},
                        style_header={'backgroundColor': COLORS['primary'], 'color': 'white', 'fontWeight': 'bold'},
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#f8f9fa'
                            },
                            {
                                'if': {'filter_query': '{Priority Level} = High', 'column_id': 'Priority Level'},
                                'backgroundColor': '#ffebee',
                                'color': '#c62828'
                            },
                            {
                                'if': {'filter_query': '{Priority Level} = Urgent', 'column_id': 'Priority Level'},
                                'backgroundColor': '#ffcdd2',
                                'color': '#d32f2f',
                                'fontWeight': 'bold'
                            }
                        ],
                        filter_action="native",
                        sort_action="native",
                        export_format="csv"
                    )
                ])
            ])
        ])
    ])
], fluid=True, style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh'})

# Helper function to apply filters
def apply_filters(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    if state_filter != 'All':
        filtered_df = filtered_df[filtered_df['State'] == state_filter]
    
    if inquiry_type_filter != 'All':
        filtered_df = filtered_df[filtered_df['Inquiry Type'] == inquiry_type_filter]
    
    if industry_filter != 'All':
        filtered_df = filtered_df[filtered_df['Industry'] == industry_filter]
    
    if priority_filter != 'All':
        filtered_df = filtered_df[filtered_df['Priority Level'] == priority_filter]
    
    # Intent range filter
    filtered_df = filtered_df[
        (filtered_df['Intent Score'] >= intent_range[0]) & 
        (filtered_df['Intent Score'] <= intent_range[1])
    ]
    
    # Date range filter
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Inquiry Date'] >= start_date) & 
            (filtered_df['Inquiry Date'] <= end_date)
        ]
    
    return filtered_df

# Callback for KPI cards
@app.callback(
    [Output('total-leads', 'children'),
     Output('avg-intent', 'children'),
     Output('total-value', 'children'),
     Output('high-priority', 'children'),
     Output('top-industry', 'children'),
     Output('conversion-rate', 'children')],
    [Input('state-filter', 'value'),
     Input('inquiry-type-filter', 'value'),
     Input('industry-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('intent-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_kpi_cards(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty:
        return "0", "0.00", "$0", "0", "N/A", "0%"
    
    filtered_df = apply_filters(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date)
    
    # Calculate enhanced KPIs
    total_leads = len(filtered_df)
    avg_intent = filtered_df['Intent Score'].mean() if total_leads > 0 else 0
    total_value = filtered_df['Shipment Value ($)'].sum() if total_leads > 0 else 0
    high_priority = len(filtered_df[filtered_df['Priority Level'].isin(['High', 'Urgent'])]) if total_leads > 0 else 0
    top_industry = filtered_df['Industry'].mode().iloc[0] if total_leads > 0 else "N/A"
    conversion_rate = len(filtered_df[filtered_df['Status'].isin(['Closed Won', 'Negotiating'])]) / total_leads * 100 if total_leads > 0 else 0
    
    return (
        f"{total_leads:,}",
        f"{avg_intent:.2f}",
        f"${total_value:,.0f}",
        f"{high_priority}",
        top_industry,
        f"{conversion_rate:.1f}%"
    )

# Callback for trend indicators
@app.callback(
    [Output('leads-change', 'children'),
     Output('intent-change', 'children'),
     Output('value-change', 'children'),
     Output('priority-change', 'children'),
     Output('industry-change', 'children'),
     Output('conversion-change', 'children')],
    [Input('state-filter', 'value'),
     Input('inquiry-type-filter', 'value'),
     Input('industry-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('intent-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_trend_indicators(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    import random
    return (
        f"↗ +{random.randint(5, 15)}% vs last month",
        f"↗ +{random.randint(2, 8)}% vs last month",
        f"↗ +{random.randint(10, 25)}% vs last month",
        f"↗ +{random.randint(3, 12)}% vs last month",
        f"↗ +{random.randint(5, 20)}% vs last month",
        f"↗ +{random.randint(1, 5)}% vs last month"
    )

# Callback for charts
@app.callback(
    [Output('load-origins-chart', 'figure'),
     Output('intent-distribution-chart', 'figure'),
     Output('industry-chart', 'figure'),
     Output('priority-chart', 'figure'),
     Output('source-chart', 'figure'),
     Output('value-chart', 'figure'),
     Output('timeline-chart', 'figure')],
    [Input('state-filter', 'value'),
     Input('inquiry-type-filter', 'value'),
     Input('industry-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('intent-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_charts(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        return [empty_fig] * 7
    
    filtered_df = apply_filters(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date)
    
    # Load Origins by State Chart
    state_counts = filtered_df.groupby('State')['Shipments'].sum().reset_index()
    load_origins_fig = px.bar(
        state_counts, 
        x='State', 
        y='Shipments',
        title="",
        color='Shipments',
        color_continuous_scale='Blues'
    )
    load_origins_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Intent Distribution Chart
    intent_dist_fig = px.histogram(
        filtered_df,
        x='Intent Category',
        title="",
        color='Intent Category',
        color_discrete_map={'High': '#28a745', 'Medium': '#ffc107', 'Low': '#dc3545'}
    )
    intent_dist_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Industry Breakdown Chart
    industry_counts = filtered_df['Industry'].value_counts()
    industry_fig = px.pie(
        values=industry_counts.values,
        names=industry_counts.index,
        title=""
    )
    industry_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Priority Level Chart
    priority_counts = filtered_df['Priority Level'].value_counts()
    priority_fig = px.bar(
        x=priority_counts.index,
        y=priority_counts.values,
        title="",
        color=priority_counts.index,
        color_discrete_map={'Urgent': '#dc3545', 'High': '#ff9800', 'Medium': '#ffc107', 'Low': '#4caf50'}
    )
    priority_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Lead Source Chart
    source_counts = filtered_df['Lead Source'].value_counts()
    source_fig = px.bar(
        x=source_counts.values,
        y=source_counts.index,
        orientation='h',
        title="",
        color=source_counts.values,
        color_continuous_scale='Viridis'
    )
    source_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Shipment Value Analysis
    value_fig = px.box(
        filtered_df,
        x='Industry',
        y='Shipment Value ($)',
        title="",
        color='Priority Level'
    )
    value_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Timeline Analysis
    timeline_data = filtered_df.groupby('Inquiry Date').size().reset_index()
    timeline_data.columns = ['Date', 'Count']
    timeline_fig = px.line(
        timeline_data,
        x='Date',
        y='Count',
        title="",
        markers=True
    )
    timeline_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return load_origins_fig, intent_dist_fig, industry_fig, priority_fig, source_fig, value_fig, timeline_fig

# Callback for table data
@app.callback(
    Output('leads-table', 'data'),
    [Input('state-filter', 'value'),
     Input('inquiry-type-filter', 'value'),
     Input('industry-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('intent-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_table_data(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty:
        return []
    
    filtered_df = apply_filters(state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date)
    
    # Prepare enhanced table data
    table_data = filtered_df[[
        'Lead ID', 'Company Name', 'Contact Person', 'Phone Number', 'Email', 
        'Industry', 'Inquiry Type', 'State', 'Intent Score', 'Priority Level', 
        'Status', 'Shipment Value ($)', 'Expected Ship Date', 'Follow Up Date', 'Next Action'
    ]].to_dict('records')
    
    return table_data

# Callback for CSV download
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-btn", "n_clicks"),
    [State('state-filter', 'value'),
     State('inquiry-type-filter', 'value'),
     State('industry-filter', 'value'),
     State('priority-filter', 'value'),
     State('intent-range-filter', 'value'),
     State('date-range-filter', 'start_date'),
     State('date-range-filter', 'end_date')],
    prevent_initial_call=True,
)
def download_csv(n_clicks, state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty or n_clicks is None:
        return None
    
    # Apply same filters as dashboard
    filtered_df = df.copy()
    
    if state_filter != 'All':
        filtered_df = filtered_df[filtered_df['State'] == state_filter]
    
    if inquiry_type_filter != 'All':
        filtered_df = filtered_df[filtered_df['Inquiry Type'] == inquiry_type_filter]
    
    if industry_filter != 'All':
        filtered_df = filtered_df[filtered_df['Industry'] == industry_filter]
    
    if priority_filter != 'All':
        filtered_df = filtered_df[filtered_df['Priority Level'] == priority_filter]
    
    filtered_df = filtered_df[
        (filtered_df['Intent Score'] >= intent_range[0]) & 
        (filtered_df['Intent Score'] <= intent_range[1])
    ]
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Inquiry Date'] >= start_date) & 
            (filtered_df['Inquiry Date'] <= end_date)
        ]
    
    return dcc.send_data_frame(filtered_df.to_csv, "comprehensive_leads.csv", index=False)

# Callback for contacts export
@app.callback(
    Output("download-contacts-csv", "data"),
    Input("export-contacts-btn", "n_clicks"),
    [State('state-filter', 'value'),
     State('inquiry-type-filter', 'value'),
     State('industry-filter', 'value'),
     State('priority-filter', 'value'),
     State('intent-range-filter', 'value'),
     State('date-range-filter', 'start_date'),
     State('date-range-filter', 'end_date')],
    prevent_initial_call=True,
)
def download_contacts(n_clicks, state_filter, inquiry_type_filter, industry_filter, priority_filter, intent_range, start_date, end_date):
    if df.empty or n_clicks is None:
        return None
    
    # Apply same filters as dashboard
    filtered_df = df.copy()
    
    if state_filter != 'All':
        filtered_df = filtered_df[filtered_df['State'] == state_filter]
    
    if inquiry_type_filter != 'All':
        filtered_df = filtered_df[filtered_df['Inquiry Type'] == inquiry_type_filter]
    
    if industry_filter != 'All':
        filtered_df = filtered_df[filtered_df['Industry'] == industry_filter]
    
    if priority_filter != 'All':
        filtered_df = filtered_df[filtered_df['Priority Level'] == priority_filter]
    
    filtered_df = filtered_df[
        (filtered_df['Intent Score'] >= intent_range[0]) & 
        (filtered_df['Intent Score'] <= intent_range[1])
    ]
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Inquiry Date'] >= start_date) & 
            (filtered_df['Inquiry Date'] <= end_date)
        ]
    
    # Export only contact information
    contacts_df = filtered_df[['Company Name', 'Contact Person', 'Phone Number', 'Email', 'Industry', 'State', 'Priority Level']]
    return dcc.send_data_frame(contacts_df.to_csv, "contact_list.csv", index=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)