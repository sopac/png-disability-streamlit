import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

#data path
#path = "/Users/sachin/Dropbox/PNG/data/"
path = "data/"
#st.set_page_config(layout="wide")

# st.html("""
#     <style>
#         .stMainBlockContainer {
#             max-width:50rem;
#         }
#     </style>
#     """
# )

#header
col1, col2 = st.columns([1,2])
col1.image(path + "logo.png")
col2.header("PNG Disability GeoData Platform", divider=True)
col2.write('''
           PNG Socio-Demographic and Economic Survey 2022 | Household Surveys (Kobo Toolbox)

           Department of Community Development and Religion           

           ''')

st.html("<hr/>")

# stats
df_national = pd.read_excel(path + "disability_national.xlsx")
df_sex = pd.read_excel(path + "disability_sex.xlsx")
df_age = pd.read_excel(path + "disability_ages.xlsx")
df_area = pd.read_excel(path + "disability_urban_rural.xlsx")
df_province = pd.read_excel(path + "disability_province.xlsx")

# spatial
gdf_province = gpd.read_file(path + "shapefiles/" + "gamma_gaussian_province.shp")
gdf_district = gpd.read_file(path + "shapefiles/" + "gamma_gaussian_district.shp")
gdf_llg = gpd.read_file(path + "shapefiles/" + "gamma_gaussian_LLG.shp")

# joins
df_province['Province'] = df_province['Province'].str.upper()
gdf_province.rename(columns={"Prov_Name": "Province"}, inplace=True)
gdf_province_disability = gdf_province.merge(df_province, on="Province")

# tables
table = st.selectbox("Select Data : ", ["National Disability", "Disability by Sex", "Disability by Age", "Disability by Area"])
header = "National Disability Overview"
df = df_national

if table == "Disability by Sex":
    df = df_sex
    header = "National Disability by Sex"

if table == "Disability by Age":
    df = df_age
    header = "National Disability by Age (yr)"

if table == "Disability by Area":
    df = df_area
    header = "National Disability by Urban or Rural"


st.subheader(header)
st.dataframe(df)

#map
map = st.selectbox("Select Map : ", ["Population Province", "Population District", "Population Local Level Government", "Disability by Province", "Disability by District *", "Disability by Local Level Government *", "Disability by Household *"])
gdf = gdf_province_disability
var = 'With Disability'
label = "Province"

if map == "Population Province":
    gdf = gdf_province
    label = "Province"
    var = "total"

if map == "Population District":
    gdf = gdf_district
    label = "Dist_Name"
    var = "total"

if map == "Population Local Level Government":
    gdf = gdf_llg
    label = "LLG_Name"
    var = "total"


fig = px.choropleth(gdf, geojson=gdf.geometry, hover_name=label, locations=gdf.index, color=gdf[var], color_continuous_scale="OrRd", projection="mercator")
fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)
st.write(gdf.drop(columns=['geometry', 'upper', 'lower']))