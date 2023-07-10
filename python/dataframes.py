from clean import read_and_clean

# Create dataframes of each dataset
economy = read_and_clean("economy")
epidemiology = read_and_clean("epidemiology")
index = read_and_clean("index")
demographic = read_and_clean("demographics")
vaccinations = read_and_clean("vaccinations")