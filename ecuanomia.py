import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import plotly.express as px

st.title('Análisis de empresas que cotizan en la Bolsa de Valores')

df = pd.read_csv('Ecuanomia - test.csv', decimal=',')
empresas = df['Empresa'].unique()
empresa = st.selectbox('Selecciona una empresa', empresas)
df_empresa = df[df['Empresa']==empresa]

fig = px.bar(df_empresa, x='Año', y='Ingresos', text='Ingresos')
fig.update_traces(textposition='outside', marker_color='royalblue')
fig.update_layout(width=600, height=500, plot_bgcolor='white', yaxis_visible=False, title_text='Ingresos (en millones de dólares)', 
                  title_x=0.5, 
                  title_font_color='gray')
fig.update_xaxes(title='', visible=True, showticklabels=True)
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df_empresa, x='Año', y='Utilidad Neta', text='Utilidad Neta')
fig.update_traces(textposition='outside', marker_color='royalblue')
fig.update_layout(width=600, height=500, plot_bgcolor='white', yaxis_visible=False, title_text='Utilidad Neta (en millones de dólares)', title_x=0.5, 
                  title_font_color='gray')
fig.update_xaxes(title='', visible=True, showticklabels=True)
st.plotly_chart(fig, use_container_width=True)

y_max_utilidad = df_empresa['Margen Bruto %'].max()*1.10

fig = px.line(df_empresa, x='Año', y=['Margen Bruto %', 'Margen Neto %'], markers=True)
fig.update_layout(width=600, height=500, plot_bgcolor='white', title_text='Utilidad (%)', title_x=0.5, 
                  title_font_color='gray', yaxis_range=[0,y_max_utilidad])
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.95, xanchor="right",x=0.7, title='', font_size=10))
fig.update_xaxes(title='', visible=True, showticklabels=True)
fig.update_yaxes(title='', visible=True, showticklabels=True, showgrid=True, gridcolor='whitesmoke', zerolinecolor = 'gray',
                 zerolinewidth=1)
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df_empresa, x='Año', y='Costo de Ventas', text='Costo de Ventas')
fig.update_traces(textposition='outside', marker_color='royalblue')
fig.update_layout(width=600, height=500, plot_bgcolor='white', yaxis_visible=False, title_text='Costos (en millones de dólares)',
                  title_x=0.5, 
                  title_font_color='gray')
fig.update_xaxes(title='', visible=True, showticklabels=True)
st.plotly_chart(fig, use_container_width=True)

fig = px.line(df_empresa, x='Año', y=['Crecimiento de Anual de Ingresos %', 'Crecimiento de Costos %'], markers=True)
fig.update_layout(width=600, height=500, plot_bgcolor='white', title_text='Cambio Anual de Ingresos y Costos', title_x=0.5, 
                  title_font_color='gray')
fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right",x=0.8, title='', font_size=10))
fig.update_xaxes(title='', visible=True, showticklabels=True)
fig.update_yaxes(title='', visible=True, showticklabels=True, showgrid=True, gridcolor='whitesmoke', zerolinecolor = 'gray',
                 zerolinewidth=1)
st.plotly_chart(fig, use_container_width=True)

y_min = df_empresa['Precio Acción'].min() - (df_empresa['Precio Acción'].min()*0.4)
y_max = df_empresa['Precio Acción'].max() + (df_empresa['Precio Acción'].max()*0.05)
fig = px.line(df_empresa, x='Año', y='Precio Acción' , markers=True)
fig.update_layout(width=600, height=500, plot_bgcolor='white', title_text='Precio de Acción ($)', title_x=0.5, 
                  title_font_color='gray', yaxis_range=[y_min,y_max])
fig.update_xaxes(title='', visible=True, showticklabels=True)
fig.update_yaxes(title='', visible=True, showticklabels=True, showgrid=True, gridcolor='whitesmoke', zerolinecolor = 'gray',
                 zerolinewidth=1)
st.plotly_chart(fig, use_container_width=True)
