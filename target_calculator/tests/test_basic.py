import pandas as pd

import statsmodels.api as sm

from ..target_calculator import calculate_slope_intercept


def test_calculate_slope_intercept():
    data_file_name = 'tests/fixtures/BostonHousePrices.csv'
    df_ = pd.read_csv(data_file_name)
    dependent = 'Value'
    independent = 'Rooms'
    y = df_[dependent]
    x = df_[independent]
    x = sm.add_constant(x)
    y_pred = calculate_slope_intercept(x, y, independent)
    assert y_pred[100] == 26.559266339961354
