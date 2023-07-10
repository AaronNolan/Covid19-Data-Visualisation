import datetime
from dataframes import epidemiology, vaccinations, demographic
import pandas as pd
from scipy import optimize
import warnings
import matplotlib.pyplot as plt
pd.options.plotting.backend = "plotly"
import plotly.express as px
import plotly.graph_objects as go

# suppress warnings
warnings.filterwarnings('ignore')

def get_outbreak_mask(data: pd.DataFrame, threshold: int = 10):
    ''' Returns a mask for > N confirmed cases '''
    return data['cumulative_confirmed'] > threshold

def exponential_function(x: float, a: float, b: float, c: float):
    ''' a * (b ^ x) + c '''
    return (a * (b ** x) + c)


# ----------------------------------- Graph 1 -----------------------------------

# Step 1: Combine all needed datasets
combinedDataset = pd.merge(epidemiology, vaccinations, on=['date', 'location_key'], how='inner')
combinedDataset = pd.merge(combinedDataset, demographic, on='location_key', how='inner')

# Step 2: Filter out countries with less than 300 daily values
count = combinedDataset['location_key'].value_counts()
sortedData = combinedDataset[~combinedDataset['location_key'].isin(count[count < 340].index)]

# Step 3: Set data index as date and group by date
df = sortedData.groupby('date').sum()

# Step 4: Calculate adult population by deducting younger ages from the total
adult_population = df.population.iloc[0] - df.population_age_00_09.iloc[0] - df.population_age_10_19.iloc[0]

# Step 5: Caluculate smoothed averages of our variables and add ratio scaling.
fully_vaccinated = df.cumulative_persons_fully_vaccinated.rolling(7).mean() / adult_population
confirmed_cases = df.new_confirmed.rolling(7).mean() / adult_population * 1_000
total_deaths = df.new_deceased.rolling(7).mean() / adult_population * 20_000

# Build Graph

##Fully Vaccinated on Line Graph.
estimate_plot = go.Line(
    x=df.index.tolist(),
    y=fully_vaccinated.tolist(),
    fill='tozeroy',
    line=dict(
        color='#47a4f5',
    ),
    name='Fully vaccinated (adults)'

)
## Confirmed COVID-19 Cases on Line Graph.
projected_plot = go.Line(
    x=df.index.tolist(),
    y=confirmed_cases.tolist(),
    fill='tozeroy',
    line=dict(
        color='#ffa600',
    ),
    name = 'Infections (per 1K)'
)
##Total Deaths on Line Graph.
confirmed_plot = go.Line(
    x=df.index.tolist(),
    y=total_deaths.tolist(),
    fill='tozeroy',
    line=dict(
            color='#ff6361',
            ),
    name = 'Deaths (per 20K)'
)
##Variant Dashed Line.
variant = go.Line(
    x=df.index.tolist(),
    y=df.index.tolist(),
    line=dict(
            color='#04070a',
            dash='dash',
            ),
    name = 'Variant'
)
##Layout parameters for the canvas the graphs are on.
layout_1 = go.Layout(
    title=dict(text='Effectiveness of the Covid-19 Vaccine vs COVID-19 Infection and Death Rates'),
    title_x=0.5,
    legend_title_text="Legend",
    margin=dict(l=50, r=50, b=50, t=100),
    xaxis=dict(title='Date',
    linecolor='#d9d9d9',
    mirror=False),
    yaxis=dict(title='Number of People',
    linecolor='#d9d9d9',
    mirror=False),
)

#Combines the graphs into a list and displays the aggregated graphs.
data = [estimate_plot, projected_plot, confirmed_plot, variant]
graph_1 = go.Figure(data=data, layout=layout_1)

#Adding GAMMA Variant Mark.
graph_1.add_vrect(
    x0="2020-11-01", x1="2020-11-01", 
    annotation_text="GAMMA", 
    annotation_position="top left",
    fillcolor="green", 
    opacity=0.5, 
    line_dash="dash",
    line_width=2)

#Adding OMICRON Variant Mark.
graph_1.add_vrect(
    x0="2021-11-24", x1="2021-11-24", 
    annotation_text="OMICRON", 
    annotation_position="top left",
    fillcolor="green", 
    opacity=0.5, 
    line_dash="dash",
    line_width=2)

graph_1.show()

# -------------------------------------------------------------------------------

# ----------------------------------- Graph 2 -----------------------------------

# Step 1: Filter Created Dataframe for necessary and cleaned values
df = df[['cumulative_confirmed', 'cumulative_deceased']]

# Step 2: Get data only after the outbreak begun
df = df[get_outbreak_mask(df)]

# Step 3: Group data by date
df = df.groupby('date').sum()


X, y = list(range(len(df))), df['cumulative_confirmed'].tolist()
params, _ = optimize.curve_fit(exponential_function, X, y, maxfev=5000)

#Step 4: Append N new days to our indices
ESTIMATE_DAYS=50
date_range = df.index.tolist()
for _ in range(ESTIMATE_DAYS): date_range.append(date_range[-1] + pd.Timedelta(days=1))

# Step 5: Perform projection with the previously estimated parameters
projected = [0] * len(X) + [exponential_function(x, *params) for x in range(len(X), len(X) + ESTIMATE_DAYS)]
projected = pd.Series(projected, index=date_range, name='Projected')
estimate = [exponential_function(x, *params) for x in range(len(date_range))]

# Build Graph
##Estimated Covid Cases on Line Graph.
estimate_plot = go.Line(
    x=date_range,
    y=estimate,
    line=dict(
        color='#ff6361',
        width=5,
    ),
    name='Estimate Infections'

)
##Projected Covid Cases on Scatter Graph.
projected_plot = go.Scatter(
    x=date_range,
    y=projected,
    fill='tozeroy',
    line=dict(
        color='rgb(237, 157, 76)',
    ),
    name = 'Projected Infections'
)
##Confirmed New Covid Cases on Scatter Graph.
confirmed_plot = go.Scatter(
    x=date_range,
    y=df['cumulative_confirmed'],
    fill='tozeroy',
    line=dict(
        color='#47a4f5',
    )  ,
    name = 'Confirmed Infections'
)




##Layout parameters for the canvas the graphs are on.
layout = go.Layout(
    title=dict(text='Exponential modeling of the growth of COVID-19 Infections'),
    title_x=0.5,
    legend_title_text="Legend",
    margin=dict(l=50, r=50, b=50, t=100),
    xaxis=dict(title='Date',
    linecolor='#d9d9d9',
    mirror=True),
    yaxis=dict(title='Number of COVID-19 Cases',
    linecolor='#d9d9d9',
    mirror=True),
)
#Combines the graphs into a list and displays the aggregated graphs.
data = [estimate_plot, projected_plot, confirmed_plot, variant]
graph_2 = go.Figure(data=data, layout=layout)

#Adding GAMMA Variant Mark.
graph_2.add_vrect(
    x0="2020-11-01", x1="2020-11-01", 
    annotation_text="GAMMA", 
    annotation_position="top left",
    fillcolor="green", 
    opacity=0.5, 
    line_dash="dash",
    line_width=2)

#Adding OMICRON Variant Mark.
graph_2.add_vrect(
    x0="2021-11-24", x1="2021-11-24", 
    annotation_text="OMICRON", 
    annotation_position="top left",
    fillcolor="green", 
    opacity=0.5, 
    line_dash="dash",
    line_width=2)


graph_2.show()
