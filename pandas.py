import pandas as pd

# -------- READ CSV --------
path_to_sampler = "https://raw.githubusercontent.com/suzannelittle/ca682i/master/data/sampler/DataSampler.csv"
df_csv = pd.read_csv(path_to_sampler)  # look at the other arguments to read_csv. Anything you could add?
df_csv.head(10)  # show the first 10 lines
df_csv.tail() # show the last 5 lines
df_csv.shape  # find out how many rows and columns
df_csv.columns # show list of column names
df_csv.info()

# -------- READ EXCEL --------
df_excel = pd.read_excel("http://www.principlesofeconometrics.com/poe5/data/excel/nasa.xlsx")
df_excel.head()
df_excel.shape
df_excel.info()
df_excel.describe()

# -------- READ JSON --------
df_json = pd.read_json("https://raw.githubusercontent.com/corysimmons/colors.json/master/colors.json")
df_json.head()
df_json.shape
df_json.transpose().head()
df_json.shape
df_json_T = df_json.T
df_json_T.shape
df_json_T.head()
