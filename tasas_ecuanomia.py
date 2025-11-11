import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Tasas pasivas de todas las entidades financieras",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Tasas pasivas de todas las entidades financieras")

url_path = "tasas_2024_forward.csv"

# Load data locally
@st.cache_data
def load_data(url_path):
    """Load data from local file and return DataFrame"""
    try:
        df = pd.read_csv(url_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data(url_path)

if df is not None:
    # Ensure month column is string format for filtering
    if 'mes' in df.columns:
        df['mes'] = df['mes'].astype(str)
    
    # Filter for month == '2025-09'
    df_filtered = df[df['mes'] == '2025-09'].copy()
    
    if len(df_filtered) > 0:
        st.sidebar.success(f"✅ Filtered {len(df_filtered)} records for month 2025-09")
        
        # Search box for razon_social
        st.sidebar.header("🔍 Filtros")
        search_text = st.sidebar.text_input(
            "Buscar por Razón Social",
            value="",
            help="Ingrese texto para buscar en razón social"
        )
        
        # Dropdown for ULTIMA_CALIFICACION
        if 'ULTIMA_CALIFICACIÓN' in df_filtered.columns:
            # Define the order of calificaciones
            calificaciones_order = [
                "AAA", "AAA-", "AA+", "AA", "AA-", 
                "A+", "A", "A-", 
                "BBB+", "BBB", "BBB-", 
                "BB+", "BB", "BB-", 
                "B+", "B", "B-"
            ]
            
            # Get unique calificaciones from data
            available_calificaciones = df_filtered['ULTIMA_CALIFICACIÓN'].dropna().unique().tolist()
            
            # Sort calificaciones according to the predefined order
            sorted_calificaciones = []
            for cal in calificaciones_order:
                if cal in available_calificaciones:
                    sorted_calificaciones.append(cal)
            
            # Add any calificaciones not in the predefined order at the end
            for cal in available_calificaciones:
                if cal not in sorted_calificaciones:
                    sorted_calificaciones.append(cal)
            
            # Add "Todos" at the beginning
            calificaciones = ['Todos'] + sorted_calificaciones
            
            selected_calificacion = st.sidebar.selectbox(
                "Filtrar por Calificación",
                options=calificaciones,
                index=0
            )
        else:
            selected_calificacion = 'Todos'
        
        # Dropdown for plazo
        if 'plazo' in df_filtered.columns:
            # Get unique plazos from data and sort them
            available_plazos = sorted(df_filtered['plazo'].dropna().unique().tolist())
            plazos = ['Todos'] + available_plazos
            
            selected_plazo = st.sidebar.selectbox(
                "Filtrar por Plazo",
                options=plazos,
                index=0
            )
        else:
            selected_plazo = 'Todos'
        
        # Apply filters
        df_filtered_search = df_filtered.copy()
        
        # Filter by search text
        if search_text:
            df_filtered_search = df_filtered_search[
                df_filtered_search['razon_social'].str.contains(
                    search_text, 
                    case=False, 
                    na=False
                )
            ]
        
        # Filter by calificación
        if selected_calificacion != 'Todos':
            df_filtered_search = df_filtered_search[
                df_filtered_search['ULTIMA_CALIFICACIÓN'] == selected_calificacion
            ]
        
        # Filter by plazo
        if selected_plazo != 'Todos':
            df_filtered_search = df_filtered_search[
                df_filtered_search['plazo'] == selected_plazo
            ]
        
        # Update sidebar info
        st.sidebar.info(f"📊 Mostrando {len(df_filtered_search)} de {len(df_filtered)} registros")
        
        # Main KPI Cards (based on filtered data)
        #st.header("📈 Tasas Pasivas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mean_tasa = df_filtered_search['tasa_pasiva_efectiva'].mean()
            st.metric(
                label="Tasa Pasiva Efectiva Promedio",
                value=f"{mean_tasa:,.2f}"
            )
        
        with col2:
            max_tasa = df_filtered_search['tasa_pasiva_efectiva'].max()
            st.metric(
                label="Tasa Pasiva Efectiva Máxima",
                value=f"{max_tasa:,.2f}"
            )
        
        with col3:
            min_tasa = df_filtered_search['tasa_pasiva_efectiva'].min()
            st.metric(
                label="Tasa Pasiva Efectiva Mínima",
                value=f"{min_tasa:,.2f}"
            )
        
        with col4:
            nunique_razon = df_filtered_search['razon_social'].nunique()
            st.metric(
                label="Número de Entidades Financieras",
                value=f"{nunique_razon:,}"
            )
        
        # Sortable Table
        st.header("📋 Todas las ofertas")
        
        # Create table with selected columns
        table_columns = ['razon_social', 'ULTIMA_CALIFICACIÓN', 'plazo', 'tasa_pasiva_efectiva']
        
        # Check if all columns exist
        missing_cols = [col for col in table_columns if col not in df_filtered_search.columns]
        if missing_cols:
            st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}")
            available_cols = [col for col in table_columns if col in df_filtered_search.columns]
            table_df = df_filtered_search[available_cols].copy()
        else:
            table_df = df_filtered_search[table_columns].copy()
        
        # Round tasa_pasiva_efectiva to 2 decimals
        if 'tasa_pasiva_efectiva' in table_df.columns:
            table_df['tasa_pasiva_efectiva'] = table_df['tasa_pasiva_efectiva'].round(2)
        
        # Sort by tasa_pasiva_efectiva in descending order
        if 'tasa_pasiva_efectiva' in table_df.columns:
            table_df = table_df.sort_values('tasa_pasiva_efectiva', ascending=False)
        
        # Format tasa_pasiva_efectiva with % suffix and rename column
        if 'tasa_pasiva_efectiva' in table_df.columns:
            table_df['tasa_pasiva_efectiva'] = table_df['tasa_pasiva_efectiva'].apply(lambda x: f"{x:.2f}%")
            table_df = table_df.rename(columns={'tasa_pasiva_efectiva': 'Tasa pasiva'})
        
        # Rename columns
        column_rename_map = {
            'razon_social': 'Entidad',
            'ULTIMA_CALIFICACIÓN': 'Calificación',
            'plazo': 'Plazo'
        }
        table_df = table_df.rename(columns=column_rename_map)
        
        # Display sortable table
        st.dataframe(
            table_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )
        
        
        
    else:
        st.warning("⚠️ No data found for month '2025-09'")
        st.info(f"Meses disponibles: {df['mes'].unique() if 'mes' in df.columns else 'N/A'}")
else:
    st.error("❌ Failed to load data. Please check the file path.")

