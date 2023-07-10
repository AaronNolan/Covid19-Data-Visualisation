drop_columns_list = {
    "economy": ['gdp_usd', 'human_capital_index'],
    "epidemiology": ['new_recovered', 'new_tested', 'cumulative_recovered','cumulative_tested'],
    "index": ['place_id', 'wikidata_id', 'datacommons_id', 'country_code', 'subregion1_code', 'subregion1_name',
            'subregion2_code', 'subregion2_name', 'locality_code', 'locality_name', 'iso_3166_1_alpha_2',
            'iso_3166_1_alpha_3', 'aggregation_level'],
    "demographics": ['population_male', 'population_female', 'population_rural', 'population_urban',
            'population_largest_city','population_clustered', 'population_density', 'human_development_index',
            'population_age_20_29', 'population_age_30_39', 'population_age_40_49', 'population_age_50_59',
            'population_age_60_69', 'population_age_70_79', 'population_age_80_and_older'],
    "vaccinations": ['new_persons_vaccinated', 'new_vaccine_doses_administered',
            'new_persons_vaccinated_pfizer', 'cumulative_persons_vaccinated_pfizer',
            'new_persons_fully_vaccinated_pfizer','cumulative_persons_fully_vaccinated_pfizer',
            'new_vaccine_doses_administered_pfizer', 'cumulative_vaccine_doses_administered_pfizer',
            'new_persons_vaccinated_moderna', 'cumulative_persons_vaccinated_moderna',
            'new_persons_fully_vaccinated_moderna', 'cumulative_persons_fully_vaccinated_moderna',
            'new_vaccine_doses_administered_moderna', 'cumulative_vaccine_doses_administered_moderna',
            'new_persons_vaccinated_janssen', 'cumulative_persons_vaccinated_janssen',
            'new_persons_fully_vaccinated_janssen', 'cumulative_persons_fully_vaccinated_janssen',
            'new_vaccine_doses_administered_janssen', 'cumulative_vaccine_doses_administered_janssen',
            'new_persons_vaccinated_sinovac', 'total_persons_vaccinated_sinovac',
            'new_persons_fully_vaccinated_sinovac', 'total_persons_fully_vaccinated_sinovac',
            'new_vaccine_doses_administered_sinovac', 'total_vaccine_doses_administered_sinovac',
            'cumulative_vaccine_doses_administered', 'cumulative_persons_vaccinated'],
}

def drop_columns(name):
    return drop_columns_list[name]