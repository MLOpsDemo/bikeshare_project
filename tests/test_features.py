
"""
Note: These tests will fail if you have not first trained the model.
"""
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import numpy as np
import pandas as pd
from bikeshare_model.config.core import config
from bikeshare_model.processing.features import Mapper
from bikeshare_model.processing.features import WeekdayImputer



def test_sesaon_mapper(sample_input_data):
    # Validate season attribute
    # make sure season field contains all suported values and those values only 
    # After mapping makes sure the field contains only those values

    season_mapping_keys = config.model_config.season_mappings.keys()
    ndx = sample_input_data.season.sort_values().unique()
    #validate input data with configured mapping
    assert  len(ndx) == len(season_mapping_keys), "Sample data does not contain all possible 'seasons'"
    nd_result = (ndx == np.array(sorted(season_mapping_keys)))
    assert len(np.unique(nd_result) == 1) & nd_result[0] == True, "Season: values in the dataset do not match configured seasons"
    #obtain row index for one season
    #pick a season and collect index for testing afterwards
    a_season = list(season_mapping_keys)[0]
    a_season_value = config.model_config.season_mappings.get(a_season)
    a_season_first_index = sample_input_data[sample_input_data['season'] == a_season].index
  


    #test mapping
    smapper = Mapper(config.model_config.season_var, config.model_config.season_mappings)
    smapper.fit(sample_input_data)
    data = smapper.transform(sample_input_data)
    assert sorted(data.season.unique().tolist()) == sorted(config.model_config.season_mappings.values()), "Season: Incorrect Mapping of  values"

    #test the mapping is correct for the selected season
    a_season_second_index = data.query('season == @a_season_value').index
    assert len(a_season_second_index) == len(a_season_first_index), "Season: Number of mapped sessions are incorrect"
    comparision = np.unique(a_season_first_index == a_season_second_index)
    assert len(comparision) == 1 & comparision[0] == True, "Season: Incorrect mapping found in the tested season " + a_season
