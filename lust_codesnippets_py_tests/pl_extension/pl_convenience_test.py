
#%%imports
import pytest
from lust_codesnippets_py.pl_extension import pl_convenience as plc

import numpy as np
import polars as pl

#%%tests
#variables used across multiple tests
df = pl.from_dicts([
    {'column_0': 1, 'column_1': 1, 'column_2': -0.8877857476301128, 'column_3': 'l'},
    {'column_0': 4, 'column_1': 2, 'column_2': -1.980796468223927, 'column_3': 'i'},
    {'column_0': 2, 'column_1': 1, 'column_2': -0.3479121493261526, 'column_3': 'l'},
    {'column_0': 1, 'column_1': 2, 'column_2': 0.15634896910398005, 'column_3': 'c'},
    {'column_0': 4, 'column_1': 2, 'column_2': 1.2302906807277207, 'column_3': 't'},
    {'column_0': 4, 'column_1': 2, 'column_2': 1.2023798487844113, 'column_3': 'q'},
    {'column_0': 4, 'column_1': 2, 'column_2': -0.3873268174079523, 'column_3': 'a'},
    {'column_0': 4, 'column_1': 2, 'column_2': -0.30230275057533557, 'column_3': 'w'},
    {'column_0': 2, 'column_1': 1, 'column_2': -1.0485529650670926, 'column_3': 'a'},
    {'column_0': 4, 'column_1': 2, 'column_2': -1.4200179371789752, 'column_3': 'g'},
    {'column_0': 2, 'column_1': 1, 'column_2': -1.7062701906250126, 'column_3': 't'},
    {'column_0': 3, 'column_1': 2, 'column_2': 1.9507753952317897, 'column_3': 'o'},
    {'column_0': 1, 'column_1': 2, 'column_2': -0.5096521817516535, 'column_3': 'k'},
    {'column_0': 4, 'column_1': 2, 'column_2': -0.4380743016111864, 'column_3': 't'},
    {'column_0': 3, 'column_1': 2, 'column_2': -1.2527953600499262, 'column_3': 'y'},
    {'column_0': 1, 'column_1': 1, 'column_2': 0.7774903558319101, 'column_3': 'i'},
    {'column_0': 1, 'column_1': 2, 'column_2': -1.6138978475579515, 'column_3': 'n'},
    {'column_0': 1, 'column_1': 1, 'column_2': -0.2127402802139687, 'column_3': 'y'},
    {'column_0': 3, 'column_1': 1, 'column_2': -0.8954665611936756, 'column_3': 'c'},
    {'column_0': 2, 'column_1': 2, 'column_2': 0.386902497859262, 'column_3': 'd'},
    {'column_0': 3, 'column_1': 2, 'column_2': -0.510805137568873, 'column_3': 'c'},
    {'column_0': 4, 'column_1': 1, 'column_2': -1.180632184122412, 'column_3': 'l'},
    {'column_0': 4, 'column_1': 2, 'column_2': -0.028182228338654868, 'column_3': 'n'},
    {'column_0': 3, 'column_1': 1, 'column_2': 0.42833187053041766, 'column_3': 'q'},
    {'column_0': 1, 'column_1': 2, 'column_2': 0.06651722238316789, 'column_3': 'i'},
    {'column_0': 2, 'column_1': 1, 'column_2': 0.3024718977397814, 'column_3': 'i'},
    {'column_0': 2, 'column_1': 1, 'column_2': -0.6343220936809636, 'column_3': 't'},
    {'column_0': 2, 'column_1': 1, 'column_2': -0.3627411659871381, 'column_3': 'i'},
    {'column_0': 2, 'column_1': 1, 'column_2': -0.672460447775951, 'column_3': 'c'},
    {'column_0': 1, 'column_1': 1, 'column_2': -0.3595531615405413, 'column_3': 'y'},
    {'column_0': 2, 'column_1': 2, 'column_2': -0.813146282044454, 'column_3': 'u'},
    {'column_0': 1, 'column_1': 2, 'column_2': -1.7262826023316769, 'column_3': 'd'},
    {'column_0': 4, 'column_1': 1, 'column_2': 0.17742614225375283, 'column_3': 'm'},
    {'column_0': 1, 'column_1': 1, 'column_2': -0.4017809362082619, 'column_3': 'o'},
    {'column_0': 4, 'column_1': 1, 'column_2': -1.6301983469660446, 'column_3': 'a'},
    {'column_0': 2, 'column_1': 2, 'column_2': 0.4627822555257742, 'column_3': 'e'},
    {'column_0': 3, 'column_1': 2, 'column_2': -0.9072983643832422, 'column_3': 'd'},
    {'column_0': 4, 'column_1': 1, 'column_2': 0.05194539579613895, 'column_3': 'n'},
    {'column_0': 4, 'column_1': 2, 'column_2': 0.7290905621775369, 'column_3': 'l'},
    {'column_0': 1, 'column_1': 1, 'column_2': 0.12898291075741067, 'column_3': 'w'},
])

class Test_cut:

    @pytest.fixture(
        params=[
            (pl.col("column_0"), [0,1,2,3,4,5], "%0.1f", "cut", False, pl.from_dicts([{'cut': '(0.0,1.0]', 'count': 11}, {'cut': '(1.0,2.0]', 'count': 10}, {'cut': '(2.0,3.0]', 'count': 6}, {'cut': '(3.0,4.0]', 'count': 13}])),
            (pl.col("column_0"), [0,1,2,3,4,5], "%0.2f", "cut", False, pl.from_dicts([{'cut': '(0.00,1.00]', 'count': 11}, {'cut': '(1.00,2.00]', 'count': 10}, {'cut': '(2.00,3.00]', 'count': 6}, {'cut': '(3.00,4.00]', 'count': 13}])),
            (pl.col("column_0"), [0,1,2,3,4,5], "%0.1f", "cut", True,  pl.from_dicts([{'cut': '[1.0,2.0)', 'count': 11}, {'cut': '[2.0,3.0)', 'count': 10}, {'cut': '[3.0,4.0)', 'count': 6}, {'cut': '[4.0,5.0)', 'count': 13}])),
            (pl.col("column_0"), [0,1,2,3,4],   "%0.1f", "cut", False, pl.from_dicts([{'cut': '(0.0,1.0]', 'count': 11}, {'cut': '(1.0,2.0]', 'count': 10}, {'cut': '(2.0,3.0]', 'count': 6}, {'cut': '(3.0,4.0]', 'count': 13}])),
            (pl.col("column_0"), [2,3,4,5],     "%0.1f", "cut", False, pl.from_dicts([{'cut': '(-inf,2.0]', 'count': 21}, {'cut': '(2.0,3.0]', 'count': 6}, {'cut': '(3.0,4.0]', 'count': 13}])),
            (pl.col("column_0"), [2,3],         "%0.1f", "cut", False, pl.from_dicts([{'cut': '(-inf,2.0]', 'count': 21}, {'cut': '(2.0,3.0]', 'count': 6}, {'cut': '(3.0,+inf]', 'count': 13}])),
            (pl.col("column_0"), [2,3],         "%0.1f", "cut", False, pl.from_dicts([{'cut': '(-inf,2.0]', 'count': 21}, {'cut': '(2.0,3.0]', 'count': 6}, {'cut': '(3.0,+inf]', 'count': 13}])),
            (pl.col("column_0"), 5,             "%0.1f", "cut", False, pl.from_dicts([{'cut': '(-inf,1.0]', 'count': 11}, {'cut': '(1.8,2.5]', 'count': 10}, {'cut': '(2.5,3.2]', 'count': 6}, {'cut': '(3.2,4.0]', 'count': 13}])),
        ]
    )
    def action(self, request):
        #arrange
        global df

        #act
        col, breaks, format, alias, left_closed, df_cut_true  = request.param
        df_cut_pred = plc.cut(df, col, breaks, format, alias, left_closed=left_closed)["cut"].value_counts().sort("cut")

        return df_cut_pred, df_cut_true

    #assert
    def test_cut(self, action):
        assert action[0].equals(action[1])

class Test_value_counts:

    @pytest.fixture(
        params=[
            ("column_0",               None,        True,  pl.from_dicts([{'column_0': 3, 'count': 6}, {'column_0': 2, 'count': 10}, {'column_0': 1, 'count': 11}, {'column_0': 4, 'count': 13}])),
            (["column_0", "column_1"], "frequency", False, pl.from_dicts([{'column_0': 1, 'column_1': 1, 'count': 0.6666666666666666}, {'column_0': 1, 'column_1': 2, 'count': 0.5555555555555556}, {'column_0': 2, 'column_1': 1, 'count': 0.7777777777777777}, {'column_0': 2, 'column_1': 2, 'count': 0.3333333333333333}, {'column_0': 3, 'column_1': 1, 'count': 0.2222222222222222}, {'column_0': 3, 'column_1': 2, 'count': 0.4444444444444444}, {'column_0': 4, 'column_1': 1, 'count': 0.4444444444444444}, {'column_0': 4, 'column_1': 2, 'count': 1.0}])),
            (["column_0", "column_1"], "pdf",       False, pl.from_dicts([{'column_0': 1, 'column_1': 1, 'count': 0.15000000000000002}, {'column_0': 1, 'column_1': 2, 'count': 0.125}, {'column_0': 2, 'column_1': 1, 'count': 0.17500000000000002}, {'column_0': 2, 'column_1': 2, 'count': 0.07500000000000001}, {'column_0': 3, 'column_1': 1, 'count': 0.05}, {'column_0': 3, 'column_1': 2, 'count': 0.1}, {'column_0': 4, 'column_1': 1, 'count': 0.1}, {'column_0': 4, 'column_1': 2, 'count': 0.225}])),
        ]
    )
    def action(self, request):
        #arrange
        global df

        #act
        subset, normalize, sort, df_vc_true  = request.param
        df_vc_pred = plc.value_counts(df, subset, normalize, sort)

        return df_vc_pred, df_vc_true

    #assert
    def test_value_counts(self, action):
        assert action[0].equals(action[1])

