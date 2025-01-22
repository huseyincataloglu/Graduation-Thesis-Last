import streamlit as st
import plotly.express as px
import pandas as pd
from app import df

st.markdown("<h1 style='text-align: left; color : red;'>Location Based Analyses</h1>",unsafe_allow_html=True)
st.markdown(
        """
        <h2 style="font-size:24px;">Welcome to the <strong style="color:red;">Locations Page</strong>!</h2>
        <p style="font-size:20px;">Here you can explore:</p>
        <ul style="font-size:18px;">
            <li>Total productions by Locations and differences between them</li>
            <li>Production change based on a specific species for variety years</li>
            <li>Compare production methods for different species</li>
        </ul>
        <p style="font-size:18px;">Use the sidebar to select locations and methods to customize your analysis and once you choose the locations and the range of years, it will effect all the graphs!</p>
        """, 
        unsafe_allow_html=True
    )


