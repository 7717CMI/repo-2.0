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

# Load the enhanced customer data
try:
    df = pd.read_csv('data/leads.csv')
    df['Date of Inquiry'] = pd.to_datetime(df['Date of Inquiry'])
    df['Expected Ship Date'] = pd.to_datetime(df['Expected Ship Date'])
    df['Follow Up Date'] = pd.to_datetime(df['Follow Up Date'])
    print(f"Loaded {len(df)} comprehensive customer records from data/leads.csv")
except FileNotFoundError:
    print("Error: data/leads.csv not found. Please ensure the data file exists.")
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

# Helper function to categorize rates
def categorize_rate(rate):
    if rate >= 3000:
        return 'High Value'
    elif rate >= 1500:
        return 'Medium Value'
    else:
        return 'Low Value'

# Add rate category to dataframe
if not df.empty:
    df['Rate Category'] = df['Rate / Quote Requested ($)'].apply(categorize_rate)

# Define the enhanced layout
app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col([
            html.H1("🚛 Comprehensive Customer Intelligence Dashboard", 
                   className="text-center mb-2", 
                   style={'color': COLORS['primary'], 'fontWeight': 'bold'}),
            html.H4("Real-time tracking of freight inquiries, client contacts, and shipment requirements", 
                   className="text-center mb-4", 
                   style={'color': COLORS['secondary']}),
            html.P("Advanced analytics for freight logistics, customer insights, and shipment optimization", 
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
                    html.H5("🔍 Advanced Customer Intelligence Filters", className="card-title mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Industry Type:", className="form-label"),
                            dcc.Dropdown(
                                id='industry-filter',
                                options=[{'label': 'All Industries', 'value': 'All'}] + 
                                       [{'label': industry, 'value': industry} for industry in sorted(df['Industry Type'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Shipment Requirement:", className="form-label"),
                            dcc.Dropdown(
                                id='shipment-filter',
                                options=[{'label': 'All Types', 'value': 'All'}] + 
                                       [{'label': req, 'value': req} for req in sorted(df['Shipment Requirement'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Commodity Type:", className="form-label"),
                            dcc.Dropdown(
                                id='commodity-filter',
                                options=[{'label': 'All Commodities', 'value': 'All'}] + 
                                       [{'label': commodity, 'value': commodity} for commodity in sorted(df['Product / Commodity Type'].unique()) if not df.empty],
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
                            html.Label("Source Country:", className="form-label"),
                            dcc.Dropdown(
                                id='source-country-filter',
                                options=[{'label': 'All Countries', 'value': 'All'}] + 
                                       [{'label': country, 'value': country} for country in sorted(df['Source Location / Country'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Destination Country:", className="form-label"),
                            dcc.Dropdown(
                                id='destination-country-filter',
                                options=[{'label': 'All Countries', 'value': 'All'}] + 
                                       [{'label': country, 'value': country} for country in sorted(df['Destination Location / Country'].unique()) if not df.empty],
                                value='All',
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Rate Range ($):", className="form-label"),
                            dcc.RangeSlider(
                                id='rate-range-filter',
                                min=df['Rate / Quote Requested ($)'].min() if not df.empty else 0,
                                max=df['Rate / Quote Requested ($)'].max() if not df.empty else 5000,
                                step=100,
                                value=[df['Rate / Quote Requested ($)'].min() if not df.empty else 0, df['Rate / Quote Requested ($)'].max() if not df.empty else 5000],
                                marks={i: f'${i:,.0f}' for i in range(0, int(df['Rate / Quote Requested ($)'].max() if not df.empty else 5000) + 1, 1000)},
                                className="mb-3"
                            )
                        ], md=3),
                        dbc.Col([
                            html.Label("Date Range:", className="form-label"),
                            dcc.DatePickerRange(
                                id='date-range-filter',
                                start_date=df['Date of Inquiry'].min() if not df.empty else datetime.now() - timedelta(days=60),
                                end_date=df['Date of Inquiry'].max() if not df.empty else datetime.now(),
                                display_format='YYYY-MM-DD',
                                className="mb-3"
                            )
                        ], md=3)
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
                    html.H2(id="total-customers", className="text-center mb-1"),
                    html.P("Total Customers", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="avg-rate", className="text-center mb-1"),
                    html.P("Avg Rate ($)", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="total-distance", className="text-center mb-1"),
                    html.P("Total Distance (Km)", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="high-priority", className="text-center mb-1"),
                    html.P("High Priority", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="top-industry", className="text-center mb-1"),
                    html.P("Top Industry", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2(id="conversion-rate", className="text-center mb-1"),
                    html.P("Conversion Rate", className="text-center text-muted mb-0")
                ])
            ], className="text-center h-100")
        ], md=2)
    ], className="mb-4"),
    
    # Enhanced Charts Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🌍 Shipment Origins by Country", className="card-title"),
                    dcc.Graph(id="source-country-chart"),
                    html.P("Geographic distribution of shipment origins across countries", 
                           className="text-muted small mt-2")
                ])
            ], className="h-100")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📦 Shipment Requirements Distribution", className="card-title"),
                    dcc.Graph(id="shipment-requirements-chart"),
                    html.P("Distribution of different shipment types and requirements", 
                           className="text-muted small mt-2")
                ])
            ], className="h-100")
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🏭 Industry Type Breakdown", className="card-title"),
                    dcc.Graph(id="industry-chart")
                ])
            ], className="h-100")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📊 Rate Value Analysis", className="card-title"),
                    dcc.Graph(id="rate-chart")
                ])
            ], className="h-100")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 Distance Distribution", className="card-title"),
                    dcc.Graph(id="distance-chart")
                ])
            ], className="h-100")
        ], md=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🚚 Commodity Type Analysis", className="card-title"),
                    dcc.Graph(id="commodity-chart")
                ])
            ], className="h-100")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📅 Inquiry Timeline", className="card-title"),
                    dcc.Graph(id="timeline-chart")
                ])
            ], className="h-100")
        ], md=6)
    ], className="mb-4"),
    
    # Enhanced Customer Table Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("👥 Comprehensive Customer Intelligence", className="card-title"),
                    html.Div([
                        dbc.Button("📥 Download CSV", id="download-btn", color="primary", className="mb-3 me-2"),
                        dbc.Button("📧 Export Contacts", id="export-contacts-btn", color="success", className="mb-3")
                    ]),
                    dcc.Download(id="download-dataframe-csv"),
                    dcc.Download(id="download-contacts-csv"),
                    dash_table.DataTable(
                        id='customers-table',
                        columns=[
                            {'name': 'Customer ID', 'id': 'Customer ID'},
                            {'name': 'Company Name', 'id': 'Company Name'},
                            {'name': 'Contact Person', 'id': 'Contact Person Name'},
                            {'name': 'Email', 'id': 'Email'},
                            {'name': 'Phone', 'id': 'Phone'},
                            {'name': 'Shipment Req.', 'id': 'Shipment Requirement'},
                            {'name': 'Commodity', 'id': 'Product / Commodity Type'},
                            {'name': 'Industry', 'id': 'Industry Type'},
                            {'name': 'Source', 'id': 'Source Location / Country'},
                            {'name': 'Destination', 'id': 'Destination Location / Country'},
                            {'name': 'Distance (Km)', 'id': 'Distance to be Covered (Km)', 'type': 'numeric', 'format': {'specifier': ',.0f'}},
                            {'name': 'Rate ($)', 'id': 'Rate / Quote Requested ($)', 'type': 'numeric', 'format': {'specifier': ',.2f'}},
                            {'name': 'Inquiry Date', 'id': 'Date of Inquiry'},
                            {'name': 'Priority', 'id': 'Priority Level'},
                            {'name': 'Status', 'id': 'Status'}
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
def apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    if industry_filter != 'All':
        filtered_df = filtered_df[filtered_df['Industry Type'] == industry_filter]
    
    if shipment_filter != 'All':
        filtered_df = filtered_df[filtered_df['Shipment Requirement'] == shipment_filter]
    
    if commodity_filter != 'All':
        filtered_df = filtered_df[filtered_df['Product / Commodity Type'] == commodity_filter]
    
    if priority_filter != 'All':
        filtered_df = filtered_df[filtered_df['Priority Level'] == priority_filter]
    
    if source_country_filter != 'All':
        filtered_df = filtered_df[filtered_df['Source Location / Country'] == source_country_filter]
    
    if destination_country_filter != 'All':
        filtered_df = filtered_df[filtered_df['Destination Location / Country'] == destination_country_filter]
    
    # Rate range filter
    filtered_df = filtered_df[
        (filtered_df['Rate / Quote Requested ($)'] >= rate_range[0]) & 
        (filtered_df['Rate / Quote Requested ($)'] <= rate_range[1])
    ]
    
    # Date range filter
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Date of Inquiry'] >= start_date) & 
            (filtered_df['Date of Inquiry'] <= end_date)
        ]
    
    return filtered_df

# Callback for KPI cards
@app.callback(
    [Output('total-customers', 'children'),
     Output('avg-rate', 'children'),
     Output('total-distance', 'children'),
     Output('high-priority', 'children'),
     Output('top-industry', 'children'),
     Output('conversion-rate', 'children')],
    [Input('industry-filter', 'value'),
     Input('shipment-filter', 'value'),
     Input('commodity-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('source-country-filter', 'value'),
     Input('destination-country-filter', 'value'),
     Input('rate-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_kpi_cards(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty:
        return "0", "$0.00", "0", "0", "N/A", "0%"
    
    filtered_df = apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date)
    
    # Calculate enhanced KPIs
    total_customers = len(filtered_df)
    avg_rate = filtered_df['Rate / Quote Requested ($)'].mean() if total_customers > 0 else 0
    total_distance = filtered_df['Distance to be Covered (Km)'].sum() if total_customers > 0 else 0
    high_priority = len(filtered_df[filtered_df['Priority Level'].isin(['High', 'Urgent'])]) if total_customers > 0 else 0
    top_industry = filtered_df['Industry Type'].mode().iloc[0] if total_customers > 0 else "N/A"
    conversion_rate = len(filtered_df[filtered_df['Status'].isin(['Closed Won', 'Negotiating'])]) / total_customers * 100 if total_customers > 0 else 0
    
    return (
        f"{total_customers:,}",
        f"${avg_rate:,.2f}",
        f"{total_distance:,.0f}",
        f"{high_priority}",
        top_industry,
        f"{conversion_rate:.1f}%"
    )

# Callback for charts
@app.callback(
    [Output('source-country-chart', 'figure'),
     Output('shipment-requirements-chart', 'figure'),
     Output('industry-chart', 'figure'),
     Output('rate-chart', 'figure'),
     Output('distance-chart', 'figure'),
     Output('commodity-chart', 'figure'),
     Output('timeline-chart', 'figure')],
    [Input('industry-filter', 'value'),
     Input('shipment-filter', 'value'),
     Input('commodity-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('source-country-filter', 'value'),
     Input('destination-country-filter', 'value'),
     Input('rate-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_charts(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        return [empty_fig] * 7
    
    filtered_df = apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date)
    
    # Source Country Chart
    source_counts = filtered_df['Source Location / Country'].value_counts()
    source_fig = px.bar(
        x=source_counts.values,
        y=source_counts.index,
        orientation='h',
        title="",
        color=source_counts.values,
        color_continuous_scale='Blues'
    )
    source_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Shipment Requirements Chart
    shipment_counts = filtered_df['Shipment Requirement'].value_counts()
    shipment_fig = px.pie(
        values=shipment_counts.values,
        names=shipment_counts.index,
        title=""
    )
    shipment_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Industry Chart
    industry_counts = filtered_df['Industry Type'].value_counts()
    industry_fig = px.bar(
        x=industry_counts.index,
        y=industry_counts.values,
        title="",
        color=industry_counts.values,
        color_continuous_scale='Viridis'
    )
    industry_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Rate Chart
    rate_fig = px.histogram(
        filtered_df,
        x='Rate / Quote Requested ($)',
        title="",
        color='Rate Category',
        color_discrete_map={'High Value': '#28a745', 'Medium Value': '#ffc107', 'Low Value': '#dc3545'}
    )
    rate_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Distance Chart
    distance_fig = px.box(
        filtered_df,
        x='Industry Type',
        y='Distance to be Covered (Km)',
        title="",
        color='Priority Level'
    )
    distance_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Commodity Chart
    commodity_counts = filtered_df['Product / Commodity Type'].value_counts()
    commodity_fig = px.bar(
        x=commodity_counts.values,
        y=commodity_counts.index,
        orientation='h',
        title="",
        color=commodity_counts.values,
        color_continuous_scale='Plasma'
    )
    commodity_fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    # Timeline Chart
    timeline_data = filtered_df.groupby('Date of Inquiry').size().reset_index()
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
    
    return source_fig, shipment_fig, industry_fig, rate_fig, distance_fig, commodity_fig, timeline_fig

# Callback for table data
@app.callback(
    Output('customers-table', 'data'),
    [Input('industry-filter', 'value'),
     Input('shipment-filter', 'value'),
     Input('commodity-filter', 'value'),
     Input('priority-filter', 'value'),
     Input('source-country-filter', 'value'),
     Input('destination-country-filter', 'value'),
     Input('rate-range-filter', 'value'),
     Input('date-range-filter', 'start_date'),
     Input('date-range-filter', 'end_date')]
)
def update_table_data(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty:
        return []
    
    filtered_df = apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date)
    
    # Prepare enhanced table data
    table_data = filtered_df[[
        'Customer ID', 'Company Name', 'Contact Person Name', 'Email', 'Phone',
        'Shipment Requirement', 'Product / Commodity Type', 'Industry Type',
        'Source Location / Country', 'Destination Location / Country',
        'Distance to be Covered (Km)', 'Rate / Quote Requested ($)',
        'Date of Inquiry', 'Priority Level', 'Status'
    ]].to_dict('records')
    
    return table_data

# Callback for CSV download
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-btn", "n_clicks"),
    [State('industry-filter', 'value'),
     State('shipment-filter', 'value'),
     State('commodity-filter', 'value'),
     State('priority-filter', 'value'),
     State('source-country-filter', 'value'),
     State('destination-country-filter', 'value'),
     State('rate-range-filter', 'value'),
     State('date-range-filter', 'start_date'),
     State('date-range-filter', 'end_date')],
    prevent_initial_call=True,
)
def download_csv(n_clicks, industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty or n_clicks is None:
        return None
    
    filtered_df = apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date)
    
    return dcc.send_data_frame(filtered_df.to_csv, "customer_intelligence.csv", index=False)

# Callback for contacts export
@app.callback(
    Output("download-contacts-csv", "data"),
    Input("export-contacts-btn", "n_clicks"),
    [State('industry-filter', 'value'),
     State('shipment-filter', 'value'),
     State('commodity-filter', 'value'),
     State('priority-filter', 'value'),
     State('source-country-filter', 'value'),
     State('destination-country-filter', 'value'),
     State('rate-range-filter', 'value'),
     State('date-range-filter', 'start_date'),
     State('date-range-filter', 'end_date')],
    prevent_initial_call=True,
)
def download_contacts(n_clicks, industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date):
    if df.empty or n_clicks is None:
        return None
    
    filtered_df = apply_filters(industry_filter, shipment_filter, commodity_filter, priority_filter, source_country_filter, destination_country_filter, rate_range, start_date, end_date)
    
    # Export only contact information
    contacts_df = filtered_df[['Company Name', 'Contact Person Name', 'Email', 'Phone', 'Industry Type', 'Source Location / Country', 'Priority Level']]
    return dcc.send_data_frame(contacts_df.to_csv, "customer_contacts.csv", index=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=True)