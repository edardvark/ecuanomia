import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Tasas pasivas de todas las entidades financieras"

# Load data
url_path = r"C:\Users\Eduardo Viteri\tasas_2024_forward.csv"

# Load data on app initialization
def load_initial_data():
    try:
        df = pd.read_csv(url_path)
        if 'mes' in df.columns:
            df['mes'] = df['mes'].astype(str)
        return df.to_dict('records')
    except Exception as e:
        return None

# Initialize data store with loaded data
initial_data = load_initial_data()

# Define the app layout
app.layout = html.Div([
    dcc.Store(id='data-store', data=initial_data),
    dcc.Location(id='url', refresh=False),
    
    # Header
    html.Div([
        html.H1("📊 Tasas pasivas de todas las entidades financieras", 
                style={'textAlign': 'center', 'marginBottom': '30px'})
    ]),
    
    # Main Container
    html.Div([
        # Desktop Filters Sidebar
        html.Div([
            html.H3("🔍 Filtros", style={'marginBottom': '20px'}),
            
            html.Label("Buscar por Razón Social", style={'fontWeight': 'bold', 'marginTop': '10px'}),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Ingrese texto para buscar...',
                style={'width': '100%', 'padding': '10px', 'marginBottom': '15px', 'boxSizing': 'border-box'}
            ),
            
            html.Label("Filtrar por Calificación", style={'fontWeight': 'bold', 'marginTop': '10px'}),
            dcc.Dropdown(
                id='calificacion-dropdown',
                placeholder='Seleccione una calificación...',
                style={'marginBottom': '15px'}
            ),
            
            html.Label("Filtrar por Plazo", style={'fontWeight': 'bold', 'marginTop': '10px'}),
            dcc.Dropdown(
                id='plazo-dropdown',
                placeholder='Seleccione un plazo...',
                style={'marginBottom': '15px'}
            ),
            
            html.Div(id='filter-info', style={'marginTop': '20px', 'padding': '10px', 
                                              'backgroundColor': '#e3f2fd', 'borderRadius': '5px'})
        ], className='filter-sidebar desktop-filter', style={'width': '25%', 'padding': '20px', 'backgroundColor': '#f5f5f5', 
                  'borderRadius': '10px', 'marginRight': '20px', 'boxSizing': 'border-box'}),
        
        # Main Content
        html.Div([
            # KPI Cards
            html.Div(id='kpi-cards', style={'marginBottom': '30px'}),
            
            # Mobile Filters (Collapsible, after KPIs)
            html.Details([
                html.Summary("🔍 Filtros", style={'fontSize': '1.2em', 'fontWeight': 'bold', 'padding': '15px', 
                                                  'backgroundColor': '#f5f5f5', 'borderRadius': '5px', 
                                                  'cursor': 'pointer', 'marginBottom': '20px'}),
                html.Div([
                    html.Label("Buscar por Razón Social", style={'fontWeight': 'bold', 'marginTop': '10px'}),
                    dcc.Input(
                        id='search-input-mobile',
                        type='text',
                        placeholder='Ingrese texto para buscar...',
                        style={'width': '100%', 'padding': '10px', 'marginBottom': '15px', 'boxSizing': 'border-box'}
                    ),
                    
                    html.Label("Filtrar por Calificación", style={'fontWeight': 'bold', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='calificacion-dropdown-mobile',
                        placeholder='Seleccione una calificación...',
                        style={'marginBottom': '15px'}
                    ),
                    
                    html.Label("Filtrar por Plazo", style={'fontWeight': 'bold', 'marginTop': '10px'}),
                    dcc.Dropdown(
                        id='plazo-dropdown-mobile',
                        placeholder='Seleccione un plazo...',
                        style={'marginBottom': '15px'}
                    ),
                    
                    html.Div(id='filter-info-mobile', style={'marginTop': '20px', 'padding': '10px', 
                                                              'backgroundColor': '#e3f2fd', 'borderRadius': '5px'})
                ], style={'padding': '15px', 'backgroundColor': '#f9f9f9', 'borderRadius': '5px'})
            ], className='mobile-filter', open=False),
            
            # Table/Cards Section
            html.H2("📋 Todas las ofertas", style={'marginBottom': '20px'}),
            
            # Desktop Table
            html.Div(id='desktop-table', className='desktop-view'),
            
            # Mobile Cards
            html.Div(id='mobile-cards', className='mobile-view')
            
        ], className='main-content', style={'width': '70%', 'boxSizing': 'border-box', 'padding': '20px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%', 'boxSizing': 'border-box'})
])

# Add custom CSS using index_string
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                box-sizing: border-box;
            }
            body {
                margin: 0;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            @media (max-width: 768px) {
                .desktop-view {
                    display: none !important;
                }
                .mobile-view {
                    display: block !important;
                }
                .desktop-filter {
                    display: none !important;
                }
                .mobile-filter {
                    display: block !important;
                }
                .filter-sidebar {
                    width: 100% !important;
                    margin-right: 0 !important;
                    margin-bottom: 20px;
                }
                .main-content {
                    width: 100% !important;
                    padding: 10px !important;
                }
                .kpi-card {
                    min-width: calc(50% - 10px) !important;
                    margin: 5px !important;
                }
            }
            @media (min-width: 769px) {
                .desktop-view {
                    display: block !important;
                }
                .mobile-view {
                    display: none !important;
                }
                .desktop-filter {
                    display: block !important;
                }
                .mobile-filter {
                    display: none !important;
                }
            }
            .kpi-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                flex: 1;
                min-width: 200px;
            }
            .kpi-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            .kpi-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
            .mobile-card {
                background: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .mobile-card-header {
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 10px;
                color: #667eea;
            }
            .mobile-card-row {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #eee;
            }
            .mobile-card-row:last-child {
                border-bottom: none;
            }
            .mobile-card-label {
                font-weight: bold;
                color: #666;
            }
            .mobile-card-value {
                color: #333;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to populate dropdowns (both desktop and mobile)
@app.callback(
    [Output('calificacion-dropdown', 'options'),
     Output('plazo-dropdown', 'options'),
     Output('calificacion-dropdown-mobile', 'options'),
     Output('plazo-dropdown-mobile', 'options')],
    Input('data-store', 'data')
)
def populate_dropdowns(data):
    if data is None:
        return [], [], [], []
    
    df = pd.DataFrame(data)
    
    # Filter for month == '2025-09'
    if 'mes' in df.columns:
        df_filtered = df[df['mes'] == '2025-09'].copy()
    else:
        df_filtered = df.copy()
    
    # Calificaciones with specific order
    calificaciones_order = [
        "AAA", "AAA-", "AA+", "AA", "AA-", 
        "A+", "A", "A-", 
        "BBB+", "BBB", "BBB-", 
        "BB+", "BB", "BB-", 
        "B+", "B", "B-"
    ]
    
    calificaciones_options = []
    if 'ULTIMA_CALIFICACIÓN' in df_filtered.columns:
        available_calificaciones = df_filtered['ULTIMA_CALIFICACIÓN'].dropna().unique().tolist()
        sorted_calificaciones = []
        for cal in calificaciones_order:
            if cal in available_calificaciones:
                sorted_calificaciones.append(cal)
        for cal in available_calificaciones:
            if cal not in sorted_calificaciones:
                sorted_calificaciones.append(cal)
        calificaciones_options = [{'label': 'Todos', 'value': 'Todos'}] + \
                                 [{'label': cal, 'value': cal} for cal in sorted_calificaciones]
    
    # Plazos
    plazos_options = []
    if 'plazo' in df_filtered.columns:
        available_plazos = sorted(df_filtered['plazo'].dropna().unique().tolist())
        plazos_options = [{'label': 'Todos', 'value': 'Todos'}] + \
                        [{'label': str(plazo), 'value': plazo} for plazo in available_plazos]
    
    return calificaciones_options, plazos_options, calificaciones_options, plazos_options

# Sync callbacks: Desktop -> Mobile
@app.callback(
    [Output('search-input-mobile', 'value'),
     Output('calificacion-dropdown-mobile', 'value'),
     Output('plazo-dropdown-mobile', 'value')],
    [Input('search-input', 'value'),
     Input('calificacion-dropdown', 'value'),
     Input('plazo-dropdown', 'value')],
    prevent_initial_call=True
)
def sync_desktop_to_mobile(search, calif, plazo):
    return search, calif, plazo

# Sync callbacks: Mobile -> Desktop
@app.callback(
    [Output('search-input', 'value'),
     Output('calificacion-dropdown', 'value'),
     Output('plazo-dropdown', 'value')],
    [Input('search-input-mobile', 'value'),
     Input('calificacion-dropdown-mobile', 'value'),
     Input('plazo-dropdown-mobile', 'value')],
    prevent_initial_call=True
)
def sync_mobile_to_desktop(search, calif, plazo):
    return search, calif, plazo

# Main callback for filtering and displaying data
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('desktop-table', 'children'),
     Output('mobile-cards', 'children'),
     Output('filter-info', 'children'),
     Output('filter-info-mobile', 'children')],
    [Input('data-store', 'data'),
     Input('search-input', 'value'),
     Input('calificacion-dropdown', 'value'),
     Input('plazo-dropdown', 'value'),
     Input('search-input-mobile', 'value'),
     Input('calificacion-dropdown-mobile', 'value'),
     Input('plazo-dropdown-mobile', 'value')]
)
def update_dashboard(data, search_text, selected_calificacion, selected_plazo, 
                     search_text_mobile, selected_calificacion_mobile, selected_plazo_mobile):
    # Use desktop values if available, otherwise use mobile (they should be synced anyway)
    search = search_text if search_text else search_text_mobile
    calif = selected_calificacion if selected_calificacion else selected_calificacion_mobile
    plazo = selected_plazo if selected_plazo else selected_plazo_mobile
    
    if data is None:
        return html.Div("Error loading data"), html.Div(), html.Div(), html.Div(), html.Div()
    
    df = pd.DataFrame(data)
    
    # Filter for month == '2025-09'
    if 'mes' in df.columns:
        df['mes'] = df['mes'].astype(str)
        df_filtered = df[df['mes'] == '2025-09'].copy()
    else:
        df_filtered = df.copy()
    
    if len(df_filtered) == 0:
        return html.Div("No data found for month '2025-09'"), html.Div(), html.Div(), html.Div(), html.Div()
    
    # Apply filters
    df_filtered_search = df_filtered.copy()
    
    # Filter by search text
    if search:
        df_filtered_search = df_filtered_search[
            df_filtered_search['razon_social'].str.contains(
                search, case=False, na=False
            )
        ]
    
    # Filter by calificación
    if calif and calif != 'Todos':
        df_filtered_search = df_filtered_search[
            df_filtered_search['ULTIMA_CALIFICACIÓN'] == calif
        ]
    
    # Filter by plazo
    if plazo and plazo != 'Todos':
        df_filtered_search = df_filtered_search[
            df_filtered_search['plazo'] == plazo
        ]
    
    # Calculate KPIs
    if 'tasa_pasiva_efectiva' in df_filtered_search.columns:
        mean_tasa = df_filtered_search['tasa_pasiva_efectiva'].mean()
        max_tasa = df_filtered_search['tasa_pasiva_efectiva'].max()
        min_tasa = df_filtered_search['tasa_pasiva_efectiva'].min()
    else:
        mean_tasa = max_tasa = min_tasa = 0
    
    if 'razon_social' in df_filtered_search.columns:
        nunique_razon = df_filtered_search['razon_social'].nunique()
    else:
        nunique_razon = 0
    
    # Create KPI cards
    kpi_cards = html.Div([
        html.Div([
            html.Div("Tasa Pasiva Efectiva Promedio", className='kpi-label'),
            html.Div(f"{mean_tasa:,.2f}", className='kpi-value')
        ], className='kpi-card', style={'flex': '1', 'minWidth': '200px'}),
        
        html.Div([
            html.Div("Tasa Pasiva Efectiva Máxima", className='kpi-label'),
            html.Div(f"{max_tasa:,.2f}", className='kpi-value')
        ], className='kpi-card', style={'flex': '1', 'minWidth': '200px'}),
        
        html.Div([
            html.Div("Tasa Pasiva Efectiva Mínima", className='kpi-label'),
            html.Div(f"{min_tasa:,.2f}", className='kpi-value')
        ], className='kpi-card', style={'flex': '1', 'minWidth': '200px'}),
        
        html.Div([
            html.Div("Número de Entidades Financieras", className='kpi-label'),
            html.Div(f"{nunique_razon:,}", className='kpi-value')
        ], className='kpi-card', style={'flex': '1', 'minWidth': '200px'})
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px'})
    
    # Prepare table data
    table_columns = ['razon_social', 'ULTIMA_CALIFICACIÓN', 'plazo', 'tasa_pasiva_efectiva']
    missing_cols = [col for col in table_columns if col not in df_filtered_search.columns]
    
    if missing_cols:
        table_df = df_filtered_search[[col for col in table_columns if col in df_filtered_search.columns]].copy()
    else:
        table_df = df_filtered_search[table_columns].copy()
    
    # Round and format
    if 'tasa_pasiva_efectiva' in table_df.columns:
        table_df['tasa_pasiva_efectiva'] = table_df['tasa_pasiva_efectiva'].round(2)
        table_df = table_df.sort_values('tasa_pasiva_efectiva', ascending=False)
        table_df['tasa_pasiva_efectiva'] = table_df['tasa_pasiva_efectiva'].apply(lambda x: f"{x:.2f}%")
    
    # Rename columns
    column_rename_map = {
        'razon_social': 'Entidad',
        'ULTIMA_CALIFICACIÓN': 'Calificación',
        'plazo': 'Plazo',
        'tasa_pasiva_efectiva': 'Tasa pasiva'
    }
    table_df = table_df.rename(columns=column_rename_map)
        
    # Desktop table
    desktop_table = dash_table.DataTable(
        data=table_df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in table_df.columns],
        sort_action='native',
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#667eea', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'whiteSpace': 'normal', 'height': 'auto'},
        page_size=20,
        style_table={'overflowX': 'auto'}
    )
    
    # Mobile cards
    mobile_cards = html.Div([
        html.Div([
            html.Div(row['Entidad'], className='mobile-card-header'),
            html.Div([
                html.Div([
                    html.Span('Calificación: ', className='mobile-card-label'),
                    html.Span(str(row.get('Calificación', 'N/A')), className='mobile-card-value')
                ], className='mobile-card-row'),
                html.Div([
                    html.Span('Plazo: ', className='mobile-card-label'),
                    html.Span(str(row.get('Plazo', 'N/A')), className='mobile-card-value')
                ], className='mobile-card-row'),
                html.Div([
                    html.Span('Tasa pasiva: ', className='mobile-card-label'),
                    html.Span(str(row.get('Tasa pasiva', 'N/A')), className='mobile-card-value',
                             style={'fontSize': '1.2em', 'fontWeight': 'bold', 'color': '#667eea'})
                ], className='mobile-card-row')
            ])
        ], className='mobile-card')
        for _, row in table_df.iterrows()
    ])
    
    # Filter info (same for both desktop and mobile)
    filter_info = html.Div([
        html.P(f"📊 Mostrando {len(df_filtered_search)} de {len(df_filtered)} registros")
    ])
    
    return kpi_cards, desktop_table, mobile_cards, filter_info, filter_info

if __name__ == '__main__':
    app.run(debug=True)
