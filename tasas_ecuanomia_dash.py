import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Tasas pasivas de todas las entidades financieras"
app.config.suppress_callback_exceptions = True

# Load data - use environment variable for production, fallback to local path
url_path = "tasas_sept_2025.csv"

# Load data on app initialization
def load_initial_data():
    try:
        df = pd.read_csv(url_path)
        if 'mes' in df.columns:
            df['mes'] = df['mes'].astype(str)
        return df
    except Exception as e:
        return None


def load_companies_data():
    try:
        companies_df = pd.read_csv("companias_2024_limpio2.csv")
        companies_df['nombre'] = companies_df['nombre'].astype(str).str.strip()
        for col in ['anio', 'ingresos_totales', 'utilidad_neta']:
            if col in companies_df.columns:
                companies_df[col] = pd.to_numeric(companies_df[col], errors='coerce')
        companies_df = companies_df.dropna(subset=['nombre', 'anio'])
        companies_df['anio'] = companies_df['anio'].astype(int)
        return companies_df
    except Exception:
        return None





def format_money_short(value):
    if pd.isna(value):
        return "$ 0"
    value = float(value)
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"$ {value / 1_000_000_000:,.2f} B"
    if abs_value >= 1_000_000:
        return f"$ {value / 1_000_000:,.2f} M"
    if abs_value >= 1_000:
        return f"$ {value / 1_000:,.2f} K"
    return f"$ {value:,.2f}"

# Initialize data store with loaded data
initial_data = load_initial_data()
companies_initial_data = load_companies_data()

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    html.Div([
        html.Div([
            html.H2("Ecuanomía", className='menu-brand'),
            dcc.RadioItems(
                id='app-menu',
                value='tasas',
                options=[
                    {'label': '📊 Tasas pasivas', 'value': 'tasas'},
                    {'label': '🏢 Compañías', 'value': 'companias'}
                ],
                className='left-menu',
                inputStyle={'marginRight': '10px'}
            )
        ], className='left-sidebar'),

        html.Div([
            # Header - tasas app
            html.Div([
                html.H1("📊 Tasas pasivas de todas las entidades financieras",
                        style={'textAlign': 'center', 'marginBottom': '30px'})
            ], id='tasas-header'),

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
                    html.Div(id='kpi-cards', style={'marginBottom': '30px'}),

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

                    html.H2("📋 Todas las ofertas", style={'marginBottom': '20px'}),
                    html.Div(id='desktop-table', className='desktop-view'),
                    html.Div(id='mobile-cards', className='mobile-view')

                ], className='main-content', style={'width': '70%', 'boxSizing': 'border-box', 'padding': '20px'})
            ], id='tasas-app-container', style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%', 'boxSizing': 'border-box'}),

            html.Div([
                html.Div([
                    html.H1("Análisis de compañías", className='companies-title'),
                    html.P("Ventas e utilidades anuales — datos Ecuanomía", className='companies-subtitle'),
                    html.Hr(className='companies-divider'),

                    html.Label("BUSCAR COMPAÑÍA", className='companies-label'),
                    dcc.Dropdown(
                        id='company-search-dropdown',
                        placeholder='Seleccione una compañía...',
                        className='companies-search'
                    ),

                    html.Div([
                        html.Div(id='selected-company-name', className='company-name-card'),
                        html.Div([
                            html.Div("VENTAS (2024)", className='metric-label'),
                            html.Div(id='company-ventas-kpi', className='metric-value ventas')
                        ], className='metric-card'),
                        html.Div([
                            html.Div("UTILIDAD NETA (2024)", className='metric-label'),
                            html.Div(id='company-utilidad-kpi', className='metric-value utilidad')
                        ], className='metric-card')
                    ], className='companies-kpi-grid'),

                    html.Div([
                        html.H3("INGRESOS TOTALES (VENTAS) POR AÑO", className='chart-title'),
                        dcc.Graph(id='company-ingresos-chart', config={'displayModeBar': False})
                    ], className='chart-container'),

                    html.Div([
                        html.H3("UTILIDAD NETA POR AÑO", className='chart-title'),
                        dcc.Graph(id='company-utilidad-chart', config={'displayModeBar': False})
                    ], className='chart-container')
                ], className='companies-app')
            ], id='companias-app-container', style={'display': 'none'})
        ], className='content-area')
    ], className='app-shell')
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
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .app-shell {
                display: flex;
                min-height: 100vh;
                background: #f4f6fa;
            }
            .left-sidebar {
                width: 260px;
                background: #0f172a;
                color: #fff;
                padding: 24px 18px;
                position: sticky;
                top: 0;
                align-self: flex-start;
                min-height: 100vh;
            }
            .menu-brand {
                margin: 0 0 24px 0;
                font-size: 1.4rem;
            }
            .left-menu label {
                display: block;
                padding: 12px 10px;
                border-radius: 8px;
                margin-bottom: 8px;
                background: #1e293b;
                cursor: pointer;
            }
            .left-menu input[type="radio"] {
                margin-right: 8px;
            }
            .content-area {
                flex: 1;
                padding: 20px;
                overflow-x: hidden;
            }
            @media (max-width: 768px) {
                .app-shell {
                    flex-direction: column;
                }
                .left-sidebar {
                    width: 100%;
                    min-height: auto;
                    position: relative;
                }
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
            .companies-app {
                background-color: #05070e;
                color: #f2f4f8;
                min-height: 100vh;
                padding: 20px;
                border-radius: 12px;
            }
            .companies-title {
                font-size: 48px;
                margin: 0;
            }
            .companies-subtitle {
                font-size: 28px;
                color: #a3adbf;
                margin-top: 8px;
            }
            .companies-divider {
                border-color: #1f2533;
                margin: 25px 0;
            }
            .companies-label {
                display: block;
                margin-bottom: 10px;
                font-size: 24px;
                letter-spacing: 1px;
                color: #b8bfce;
                font-weight: 700;
            }
            .companies-search .Select-control,
            .companies-search .Select-menu-outer,
            .companies-search .Select-placeholder,
            .companies-search .Select-value-label {
                background-color: #101522 !important;
                color: #f2f4f8 !important;
                border-color: #222a3d !important;
                font-size: 24px;
            }
            .companies-kpi-grid {
                display: grid;
                grid-template-columns: 2fr 1fr 1fr;
                gap: 20px;
                margin-top: 25px;
                margin-bottom: 25px;
            }
            .company-name-card,
            .metric-card {
                background-color: #111522;
                border: 1px solid #1f2533;
                border-radius: 14px;
                padding: 24px;
            }
            .company-name-card {
                border-left: 4px solid #20d16b;
                font-size: 44px;
                font-weight: 700;
                display: flex;
                align-items: center;
            }
            .metric-label {
                color: #a3adbf;
                font-size: 26px;
                margin-bottom: 10px;
                font-weight: 700;
            }
            .metric-value {
                font-size: 56px;
                font-weight: 800;
            }
            .metric-value.ventas {
                color: #f2f4f8;
            }
            .metric-value.utilidad {
                color: #20d16b;
            }
            .chart-container {
                background-color: #111522;
                border: 1px solid #1f2533;
                border-radius: 18px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .chart-title {
                color: #a3adbf;
                font-size: 30px;
                margin: 0 0 10px 0;
            }
            @media (max-width: 1200px) {
                .companies-kpi-grid {
                    grid-template-columns: 1fr;
                }
                .company-name-card {
                    font-size: 30px;
                }
                .metric-value {
                    font-size: 38px;
                }
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




@app.callback(
    [Output('tasas-header', 'style'),
     Output('tasas-app-container', 'style'),
     Output('companias-app-container', 'style')],
    Input('app-menu', 'value')
)
def toggle_apps(selected_app):
    tasas_visible = {'display': 'block'} if selected_app == 'tasas' else {'display': 'none'}
    tasas_container = {
        'display': 'flex' if selected_app == 'tasas' else 'none',
        'flexWrap': 'wrap',
        'width': '100%',
        'boxSizing': 'border-box'
    }
    companias_visible = {'display': 'block'} if selected_app == 'companias' else {'display': 'none'}
    return tasas_visible, tasas_container, companias_visible


@app.callback(
    Output('company-search-dropdown', 'options'),
    Input('app-menu', 'value')
)
def populate_company_dropdown(_selected_app):
    if companies_initial_data is None:
        return []
    companies_df = companies_initial_data
    company_names = sorted(companies_df['nombre'].dropna().unique())
    return [{'label': name, 'value': name} for name in company_names]


@app.callback(
    [Output('company-search-dropdown', 'value'),
     Output('selected-company-name', 'children'),
     Output('company-ventas-kpi', 'children'),
     Output('company-utilidad-kpi', 'children'),
     Output('company-ingresos-chart', 'figure'),
     Output('company-utilidad-chart', 'figure')],
    [Input('app-menu', 'value'),
     Input('company-search-dropdown', 'value')]
)
def update_companies_dashboard(_selected_app, selected_company):
    empty_fig = go.Figure().update_layout(
        paper_bgcolor='#111522',
        plot_bgcolor='#111522',
        font={'color': '#d0d6e2'}
    )

    if companies_initial_data is None:
        return None, 'Sin datos disponibles', '$ 0', '$ 0', empty_fig, empty_fig

    companies_df = companies_initial_data

    if not selected_company:
        top_2024 = companies_df[companies_df['anio'] == 2024].sort_values('ingresos_totales', ascending=False)
        selected_company = top_2024.iloc[0]['nombre'] if len(top_2024) > 0 else companies_df.iloc[0]['nombre']

    company_df = companies_df[companies_df['nombre'] == selected_company].copy()
    company_df = company_df.sort_values('anio')

    company_2024 = company_df[company_df['anio'] == 2024]
    ventas_2024 = company_2024['ingresos_totales'].iloc[0] if len(company_2024) > 0 else company_df['ingresos_totales'].iloc[-1]
    utilidad_2024 = company_2024['utilidad_neta'].iloc[0] if len(company_2024) > 0 else company_df['utilidad_neta'].iloc[-1]

    ingresos_fig = go.Figure(
        data=[go.Bar(
            x=company_df['anio'],
            y=company_df['ingresos_totales'],
            marker_color='#20d16b'
        )]
    )
    ingresos_fig.update_layout(
        paper_bgcolor='#111522',
        plot_bgcolor='#111522',
        font={'color': '#d0d6e2', 'size': 16},
        xaxis=dict(title='', gridcolor='#2a3248'),
        yaxis=dict(title='', gridcolor='#2a3248', tickprefix='$ '),
        margin=dict(l=30, r=20, t=10, b=30)
    )

    utilidad_fig = go.Figure(
        data=[go.Bar(
            x=company_df['anio'],
            y=company_df['utilidad_neta'],
            marker_color='#20d16b'
        )]
    )
    utilidad_fig.update_layout(
        paper_bgcolor='#111522',
        plot_bgcolor='#111522',
        font={'color': '#d0d6e2', 'size': 16},
        xaxis=dict(title='', gridcolor='#2a3248'),
        yaxis=dict(title='', gridcolor='#2a3248', tickprefix='$ '),
        margin=dict(l=30, r=20, t=10, b=30)
    )

    return (
        selected_company,
        selected_company,
        format_money_short(ventas_2024),
        format_money_short(utilidad_2024),
        ingresos_fig,
        utilidad_fig
    )

# Callback to populate dropdowns (both desktop and mobile)
@app.callback(
    [Output('calificacion-dropdown', 'options'),
     Output('plazo-dropdown', 'options'),
     Output('calificacion-dropdown-mobile', 'options'),
     Output('plazo-dropdown-mobile', 'options')],
    Input('app-menu', 'value')
)
def populate_dropdowns(_selected_app):
    if initial_data is None:
        return [], [], [], []

    df = initial_data.copy()
    
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
    [Input('app-menu', 'value'),
     Input('search-input', 'value'),
     Input('calificacion-dropdown', 'value'),
     Input('plazo-dropdown', 'value'),
     Input('search-input-mobile', 'value'),
     Input('calificacion-dropdown-mobile', 'value'),
     Input('plazo-dropdown-mobile', 'value')]
)
def update_dashboard(_selected_app, search_text, selected_calificacion, selected_plazo, 
                     search_text_mobile, selected_calificacion_mobile, selected_plazo_mobile):
    # Use desktop values if available, otherwise use mobile (they should be synced anyway)
    search = search_text if search_text else search_text_mobile
    calif = selected_calificacion if selected_calificacion else selected_calificacion_mobile
    plazo = selected_plazo if selected_plazo else selected_plazo_mobile
    
    if initial_data is None:
        return html.Div("Error loading data"), html.Div(), html.Div(), html.Div(), html.Div()

    df = initial_data.copy()
    
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

# Expose server for gunicorn
server = app.server

if __name__ == '__main__':
    app.run(debug=True)



