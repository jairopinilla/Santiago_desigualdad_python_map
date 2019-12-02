import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale
from matplotlib.colors import rgb2hex
import mapclassify
import adjustText as aT
import matplotlib as mpl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
import plotly.figure_factory as ff

# incorporamos geopandas! geografía + pandas :)
import geopandas as gpd
from sklearn.preprocessing import normalize

#https://plot.ly/python/v3/table/
#https://seaborn.pydata.org/tutorial/color_palettes.html
#http://colorbrewer2.org/#type=sequential&scheme=Greens&n=3
numeroRegion=13
numeroDivisiones=4
fontSizeTitulo=40
fontSizeEnMapa=14
Zoom=3
scheme='Fisher_Jenks'

dataProsupuestoMunicipal = pd.read_excel('data/datos_municipales_Disponibilidad_Presupuesto_PerCapita.xls')
#dataProsupuestoMunicipal.head()

dataPobreza = pd.read_excel('data/Indice_Pobreza_Porcentaje_Casem2018.xlsx')
#dataPobreza.head()

zonas_eod = gpd.read_file('data/Comunas', encoding="utf-8",converters={'cod_comuna':str})
zonas_eod.head()

dataset = pd.merge(zonas_eod, dataPobreza, left_on='cod_comuna',right_on='CODIGO',how='inner') 
dataset = pd.merge(dataset, dataProsupuestoMunicipal, left_on='cod_comuna',right_on='CODIGO',how='inner') 

############
codigoRegion=13
datasetRegion=dataset[dataset['codregion']==numeroRegion]
datasetRegion=datasetRegion.reset_index()
datasetRegion['Indice'] = datasetRegion.index
#datasetRegion.head()

datasetRegion["center"] = datasetRegion["geometry"].centroid
datasetRegion_points = datasetRegion.copy()
datasetRegion_points.set_geometry("center", inplace = True)

len(datasetRegion)

datasetRegion['IndiceNombre']=datasetRegion['Indice'].map(str) +':'+ datasetRegion['Comuna']

fig = go.Figure(data=[go.Table(
    header=dict(values=list(datasetRegion[['Comuna']].columns),
                fill_color='lightskyblue',
                line_color='#87CEEB',
                align='left'),
    cells=dict(values=[datasetRegion.IndiceNombre],
               fill_color='white',
                line_color='#87CEEB',
               align='left'))
])

fig.update_layout(width=320, height= (26 * len(datasetRegion) ), font=dict(
        family="Courier New, monospace",
        size=14,
        color="black"
    )     )
fig.show()
