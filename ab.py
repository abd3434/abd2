# -*- coding: utf-8 -*-
"""Untitled33.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jViVvTe7PIBxa1Trwz9oBv8lQqDANjMd
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Read the dataset into a DataFrame
df = pd.read_csv("diabetes.csv")

# Page title
st.title("Diabetes Data Visualization")

# Description
st.write("Note that through the visualization Outcome refers to whether the patient is Diabetic or not where 1 means that the patient is diabetic and 0 means that the patient is not diabetic.")

# Display files and available disk space
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded file preview:")
    st.write(df.head())

# Interactive Widgets
widget_states = {
    "Show Age Distribution by Outcome (Histogram)": st.checkbox,
    "Show 3D Scatter Plot showing relationship between Age, BMI, Glucose, and Outcome": st.checkbox,
    "Show Glucose, BMI with Age and Pregnancies Transformations vs Outcome": st.checkbox,
    "Show Animated Scatter Plot of BMI vs. Diabetes Outcome with Insulin level in Animation": st.checkbox,
    "Show Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)": st.checkbox,
}

selected_widgets = {key: value(key) for key, value in widget_states.items()}

# Filter data based on user selection
filter_column = st.selectbox("Select a Column to Filter", df.columns)
filter_value = st.text_input(f"Enter a Value to Filter {filter_column}", "")
if filter_value:
    df = df[df[filter_column] == filter_value]

# Visualizations
def show_age_distribution():
    st.subheader("Age Distribution by Outcome (Histogram)")
    fig_age_distribution = px.histogram(df, x='Age', color='Outcome', title='Age Distribution by Outcome')
    st.plotly_chart(fig_age_distribution)

def show_3d_scatter():
    st.subheader("3D Scatter Plot showing relationship between Age, BMI, Glucose, and Outcome")
    fig_3d_scatter = px.scatter_3d(df, x='Glucose', y='BMI', z='Age', color='Outcome',
                                    title='3D Scatter Plot showing relationship between Age, BMI, Glucose, and Outcome')
    st.plotly_chart(fig_3d_scatter)

def show_transformations():
    st.subheader("Glucose, BMI with Age and Pregnancies Transformations vs Outcome")
    fig_transformations = px.scatter(df, x='Glucose', y='BMI', color='Age', size='Pregnancies',
                                     title='Glucose, BMI with Age and Pregnancies Transformations vs Outcome',
                                     labels={'Glucose': 'Glucose Level', 'BMI': 'BMI'},
                                     hover_name='Outcome')
    st.plotly_chart(fig_transformations)

def show_animated_scatter():
    st.subheader("Animated Scatter Plot of BMI vs. Diabetes Outcome with Insulin level in Animation")
    # Sort the DataFrame by the "Insulin" column in increasing order
    df_sorted = df.sort_values(by="Insulin")

    # Create an animated scatter plot with Age, Outcome, and Insulin
    fig_animated = px.scatter(df_sorted, x="BMI", y="Outcome", animation_frame="Insulin", animation_group="Outcome",
                              size="BMI", color="BMI",
                              labels={"Age": "Age", "Outcome": "Diabetes Outcome", "Insulin": "Insulin"},
                              title="Animated Scatter Plot of BMI vs. Diabetes Outcome with Insulin level in Animation")

    # Customize the appearance of the plot (optional)
    fig_animated.update_traces(marker=dict(size=10),
                                selector=dict(mode='markers+text'))

    st.plotly_chart(fig_animated)

def show_density_heatmap():
    st.subheader("Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)")
    fig_density_heatmap = px.density_heatmap(df[df['Outcome'] == 0], x='DiabetesPedigreeFunction', y='BMI',
                                             labels={'DiabetesPedigreeFunction': 'Diabetes Pedigree Function', 'BMI': 'BMI'},
                                             title='Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)')
    st.plotly_chart(fig_density_heatmap)

# Show visualizations based on selected widgets
for widget, selected in selected_widgets.items():
    if selected:
        widget_functions = {
            "Show Age Distribution by Outcome (Histogram)": show_age_distribution,
            "Show 3D Scatter Plot showing relationship between Age, BMI, Glucose, and Outcome": show_3d_scatter,
            "Show Glucose, BMI with Age and Pregnancies Transformations vs Outcome": show_transformations,
            "Show Animated Scatter Plot of BMI vs. Diabetes Outcome with Insulin level in Animation": show_animated_scatter,
            "Show Density Heatmap of Diabetes Pedigree Function vs. BMI (When non-Diabetic)": show_density_heatmap,
        }
        widget_functions[widget]()