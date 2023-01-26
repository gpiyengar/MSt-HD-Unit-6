#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:44:20 2023

@author: iyengar
"""

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

#read in data from SQL
df_uns = pd.read_csv("DM labs SI.csv")
df_uns.drop_duplicates()
df = df_uns.pivot_table(index='patient', columns='observation_description', values='observation_value')


#create dashboard elements
app = Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
title = dcc.Markdown(children='# Quality Measures in Diabetes Mellitus Care')
dropdown = dcc.Dropdown(options=['HbA1c','LDL','AC Ratio','eGFR','eGFR x AC Ratio','HbA1c x LDL'],
                        value='HbA1c',
                        clearable=False)
graph = dcc.Graph(figure={})

#create layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([title], width=9)],justify='center'),
    dbc.Row([
        dbc.Col([dropdown],width=2)], justify='center'),
    dbc.Row([
        dbc.Col([graph], width=12)]),
    ], fluid=True)

#callbacks
@app.callback(
    Output(graph, component_property='figure'),
    Input(dropdown, component_property='value')
    )

#create plot options
def update_graph(user_input):
    # outpute histograms and scatters by user input
    if user_input == 'HbA1c':
        fig = px.histogram(data_frame=df, x='Hemoglobin A1c/Hemoglobin.total in Blood', 
                           color_discrete_sequence=['#4da6ff'],
                           template='simple_white',
                           labels={"Hemoglobin A1c/Hemoglobin.total in Blood": "Hemoglobin A1c (%)"})
        fig.update_layout(yaxis_title="Number of Patients", paper_bgcolor='rgba(0,0,0,0)')
        #shade by at or above target per guidelines
        fig.add_vrect(x0=0, x1=7,fillcolor="lime",opacity=0.25, layer="below", line_width=0, annotation_text="At Target", annotation_position="top left")
        fig.add_vrect(x0=7, x1=11,fillcolor="lightsalmon",opacity=0.25,layer="below", line_width=0, annotation_text="Above Target", annotation_position="top right")
        #line to delineate target
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', 
            x0=7, y0=0, x1=7, y1=1, xref='x', yref='paper')        
        
    elif user_input == 'LDL':
        fig = px.histogram(data_frame=df, x='Low Density Lipoprotein Cholesterol', 
                           color_discrete_sequence=['#4da6ff'],
                           template='simple_white',
                           labels={"Low Density Lipoprotein Cholesterol": "LDL (mmol/L)"})
        fig.update_layout(yaxis_title="Number of Patients", paper_bgcolor='rgba(0,0,0,0)')
        #shade by at or above target per guidelines
        fig.add_vrect(x0=0, x1=2,fillcolor="lime",opacity=0.25, layer="below", line_width=0, annotation_text="At Target", annotation_position="top left")
        fig.add_vrect(x0=2, x1=7,fillcolor="lightsalmon",opacity=0.25,layer="below", line_width=0, annotation_text="Above Target", annotation_position="top right")
        #line to delineate target
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', 
            x0=2, y0=0, x1=2, y1=140, xref='x', yref='y')
        
    elif user_input == 'AC Ratio':
        fig = px.histogram(data_frame=df, x='Microalbumin Creatinine Ratio',
                           color_discrete_sequence=['#4da6ff'],
                           template='simple_white',
                           labels={'Microalbumin Creatinine Ratio': 'Microalbumin Creatinine Ratio (mg/mmol)'})
        fig.add_vrect(x0=-1, x1=3,fillcolor="lime",opacity=0.25, layer="below", line_width=0, annotation_text="A1", annotation_position="top left")
        fig.add_vrect(x0=3, x1=30,fillcolor="gold",opacity=0.25, layer="below", line_width=0, annotation_text="A2", annotation_position="top left")
        fig.add_vrect(x0=30, x1=59,fillcolor="lightsalmon",opacity=0.25,layer="below", line_width=0, annotation_text="A3", annotation_position="top left")
        fig.update_layout(yaxis_title="Number of Patients", paper_bgcolor='rgba(0,0,0,0)')
        
    elif user_input == 'eGFR':
        fig = px.histogram(data_frame=df, x='Estimated Glomerular Filtration Rate', 
                           color_discrete_sequence=['#4da6ff'],
                           template='simple_white',
                           labels={'Estimated Glomerular Filtration Rate': 'Estimated Glomerular Filtration Rate (ml/min/1.73m2)'})
        #shade by CKD stage
        fig.add_vrect(x0=90, x1=170,fillcolor="lime",opacity=0.25, layer="below", line_width=0, annotation_text="Stage 1 (G1)", annotation_position="top left")
        fig.add_vrect(x0=60, x1=90,fillcolor="gold",opacity=0.25,layer="below", line_width=0, annotation_text="Stage 2 (G2)", annotation_position="top left")
        fig.add_vrect(x0=30, x1=60,fillcolor="darkOrange",opacity=0.25,layer="below", line_width=0, annotation_text="Stage 3 (G3)", annotation_position="top left")
        fig.add_vrect(x0=15, x1=30,fillcolor="lightSalmon",opacity=0.25,layer="below", line_width=0, annotation_text="Stage 4 (G4)", annotation_position="top left")
        fig.add_vrect(x0=0, x1=15,fillcolor="darkRed",opacity=0.25,layer="below", line_width=0, annotation_text="Stage 5 (G5)", annotation_position="top left")
        fig.update_layout(yaxis_title="Number of Patients", paper_bgcolor='rgba(0,0,0,0)')
        
    elif user_input =='eGFR x AC Ratio':
        fig = px.scatter(data_frame=df, x='Estimated Glomerular Filtration Rate', y='Microalbumin Creatinine Ratio',
                 hover_name="MRN: " + df.index,
                 template='simple_white',
                 color_discrete_sequence=['#4da6ff'],
                 labels={'Estimated Glomerular Filtration Rate': 'Estimated Glomerular Filtration Rate (ml/min/1.73m2)', 'Microalbumin Creatinine Ratio': 'Microalbumin Creatinine Ratio (mg/mmol)'})
        # add cut off lines 
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', #cutoff is a judgement call
            x0=60, y0=-4, x1=60, y1=63, xref='x', yref='y')
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', 
            x0=-5, y0=3, x1=161, y1=3, xref='x', yref='y')
        # shade quadrants
        fig.add_shape(
            type='rect', fillcolor="lime",opacity=0.25, layer="below", line_width=0,
            x0=60, y0=-4, x1=161, y1=3)
        fig.add_shape(
            type='rect', fillcolor="gold",opacity=0.25, layer="below", line_width=0,
            x0=60, y0=3, x1=161, y1=63)
        fig.add_shape(
            type='rect', fillcolor="gold",opacity=0.25, layer="below", line_width=0,
            x0=-5, y0=-4, x1=60, y1=3)
        fig.add_shape(
            type='rect', fillcolor="lightsalmon",opacity=0.25, layer="below", line_width=0,
            x0=-5, y0=3, x1=60, y1=63)        
        # add labels for quadrants
        fig.add_annotation(x=0, y=0, text="eGFR Low", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0, y=1, text="eGFR Low and AC Ratio Above Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0.95, y=0, text="eGFR Normal and AC Ratio at Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0.95, y=1, text="AC Ratio Above Target", xref="paper", yref="paper", showarrow=False, font_size=12)

    
    elif user_input =='HbA1c x LDL':
        fig = px.scatter(data_frame=df, x='Hemoglobin A1c/Hemoglobin.total in Blood', y='Low Density Lipoprotein Cholesterol',
                 hover_name="MRN: " + df.index, #identify the patient by MRN
                 template='simple_white',
                 color_discrete_sequence=['#4da6ff'],
                 labels={"Hemoglobin A1c/Hemoglobin.total in Blood": "Hemoglobin A1c (%)", "Low Density Lipoprotein Cholesterol": "LDL (mmol/L)"})
        # add cut off lines per guidlines to help identify people above target
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', 
            x0=7, y0=-0.4, x1=7, y1=7.5, xref='x', yref='y')
        fig.add_shape(
            type='line', line_color='midnightBlue', line_width=1, opacity=1, line_dash='dot', 
            x0=0, y0=2, x1=10.5, y1=2, xref='x', yref='y')
        # shade quadrants to improve readability 
        fig.add_shape(
            type='rect', fillcolor="lime",opacity=0.25, layer="below", line_width=0,
            x0=0, y0=-0.4, x1=7, y1=2)
        fig.add_shape(
            type='rect', fillcolor="gold",opacity=0.25, layer="below", line_width=0,
            x0=0, y0=2, x1=7, y1=7.5)
        fig.add_shape(
            type='rect', fillcolor="gold",opacity=0.25, layer="below", line_width=0,
            x0=7, y0=-0.4, x1=10.5, y1=2)
        fig.add_shape(
            type='rect', fillcolor="lightsalmon",opacity=0.25, layer="below", line_width=0,
            x0=7, y0=2, x1=10.5, y1=7.5)
        # add labels for quadrants
        fig.add_annotation(x=0, y=0, text="Both at Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0, y=1, text="LDL Above Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0.99, y=0, text="HbA1c Above Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        fig.add_annotation(x=0.99, y=1, text="Both Above Target", xref="paper", yref="paper", showarrow=False, font_size=12)
        
    return fig

#run it
if __name__ == '__main__':
    app.run_server(debug=True)