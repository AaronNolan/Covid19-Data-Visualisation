import pandas as pd
from dataframes import economy, vaccinations, demographic, epidemiology
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def calculate_gdp_per_capita_group(df):
    df = df.sort_values("gdp_per_capita_usd") # Low to High

    third_of_countries = int(df.shape[0] / 3) # Divides total number of countries by 3

    high_rate = int(df.iloc[third_of_countries * 2]["gdp_per_capita_usd"]) # Gets the lowest thirds gdp
    low_rate = int(df.iloc[third_of_countries]["gdp_per_capita_usd"]) # Gets the highest thirds gdp

    def group_gdp_per_capita_usd(row):
        if(row["gdp_per_capita_usd"] <= low_rate):
            return "1. Low (" + "<= $" + str(low_rate) + ")"
        elif(row["gdp_per_capita_usd"] >= high_rate):
            return "3. High (" + ">= $" + str(high_rate) + ")"
        else:
            return "2. Mid (" + "$"+ str(low_rate) + "- $" + str(high_rate) + ")"

    df['gdp_per_capita_usd_group'] = df.apply(lambda row: group_gdp_per_capita_usd(row), axis=1)
    return df

def calculate_adult_population(row):
    return row.population - (row.population_age_00_09 + row.population_age_10_19)

# ----------------------------------------- Querying Process -----------------------------------------
# Step 1: Get GDP Groups for Economy DF
economy = calculate_gdp_per_capita_group(economy)

# Step 2: Get Adult Population and drop other columns
demographic["population"] = demographic.apply(lambda row: calculate_adult_population(row), axis=1)

# Step 3: Drop all no longer needed columns
economy = economy.drop(labels="gdp_per_capita_usd", axis=1).dropna()
demographic = demographic.drop(labels=["population_age_00_09", "population_age_10_19"], axis=1).dropna()
epidemiology = epidemiology.drop(labels=["cumulative_confirmed", "cumulative_deceased"], axis=1).dropna()
vaccinations = vaccinations.drop(labels=["cumulative_persons_fully_vaccinated"], axis=1).dropna()

# Step 4: Merge All dataframes
epidemiology_vaccinations = pd.merge(epidemiology, vaccinations, on=["location_key", "date"], how="inner")
economy_demographic = pd.merge(economy, demographic, on="location_key", how="inner")
all_data = pd.merge(epidemiology_vaccinations, economy_demographic, on="location_key", how="inner")

# Step 5: Get most reliable months of data
all_data = all_data[(all_data.date >= '2021-02-01') & (all_data.date <= '2022-12-31')]

# Step 6: Calculate factors as percentage of population
all_data["new_deceased"] = all_data.apply(lambda row: (row.new_deceased / row.population) * 100, axis=1)
all_data["new_confirmed"] = all_data.apply(lambda row: (row.new_confirmed / row.population) * 100, axis=1)
all_data["new_persons_fully_vaccinated"] = all_data.apply(lambda row: (row.new_persons_fully_vaccinated / row.population) * 100, axis=1)
all_data["date"] = all_data.apply(lambda row: row.date.strftime("%Y-%m"), axis=1)

# Step 7: Rename columns and drop all no longer needed columns
all_data = all_data.rename(
    columns={
        "date": "Date",
        "gdp_per_capita_usd_group": "GDP per Capita Group",
        "new_persons_fully_vaccinated": "Avg Vaccinations",
        "new_deceased": "Avg Deaths",
        "new_confirmed": "Avg Infections",
    }
)
all_data = all_data.drop(labels=["population", "location_key"], axis=1)

# Step 8: Group all data by gdp group and date
all_data = all_data.groupby(["Date", "GDP per Capita Group"]).mean().reset_index()

# ----------------------------------------- Querying Process End-----------------------------------------

# ----------------------------------------- Graph -----------------------------------------

# Reference: https://plotly.com/python/animations/
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

tabs_styles = {
    'height': '44px',
    'width': "800px",
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div(children=[
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Vaccinations', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Deaths', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Infections', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dcc.Graph(
                figure= px.bar(
                    all_data,
                    x="GDP per Capita Group",
                    y="Avg Vaccinations",
                    color="GDP per Capita Group",
                    animation_frame="Date",
                    height=500,
                    width=800,
                    title="GDP vs Average Vaccinations",
                    range_y=[0, 1],
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                )
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                figure = px.bar(
                    all_data,
                    x="GDP per Capita Group",
                    y="Avg Deaths",
                    color="GDP per Capita Group",
                    animation_frame="Date",
                    height=500,
                    width=800,
                    title="GDP vs Average Deaths",
                    range_y=[0, 0.0007],
                    color_discrete_sequence=px.colors.sequential.Blues_r
                ),
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            dcc.Graph(
                figure = px.bar(
                    all_data,
                    x="GDP per Capita Group",
                    y="Avg Infections",
                    color="GDP per Capita Group",
                    animation_frame="Date",
                    height=500,
                    width=800,
                    title="GDP vs Average Infections",
                    range_y=[0, 0.25],
                    color_discrete_sequence=px.colors.sequential.Blues_r,
                ),
            )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
# ----------------------------------------- Graph Built-----------------------------------------
