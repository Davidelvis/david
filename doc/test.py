"""
 Test Functions for vectorised performance calculations.
© Copyright 2020 InferStat All or parts of this software may not be distributed, copied or re-used without the express,
 written permission of either the CEO of InferStat or an authorised representative.

Created by: David Elvis
Created date: 12/01/2020
"""

# Third library (not InferStat)
import pytest
import numpy as np
import pandas as pd

# InferStat packages
from inferlib.commonclasses.SeriesEnum import SeriesEnum
from inferlib.performance.portfolio_performance import (
    BANKRUPTCY_TIME_PENALTY,
    _cumulative_return_if_bankrupt,
    check_if_should_skip_return_calculation,
)
from inferlib.performance import vectorised
from inferlib.performance.adjusted import returns_key
from inferlin.performance.vectorised import _calc_ratio_of_return

def test_adjust_returns_for_any_bankruptcies():
    """Ensure that the returns for any bankruptcies are adjusted correctly."""
    """This statement checks if the returns_key in positions_df is < 0"""
    assert positions_df[returns_key] <0



def test_returns_for_any_bankruptcies_should_be_pdDataFrame(params):
    """Test returns will raise an error if input is not pd.DataFrame."""
    params["positions_df"] = pd.DataFrame
    with pytest.raises(TypeError):
        _calc_ratio_of_return(**params)
def test_daily_strategy_fee_not_float_error(params):
    """Test daily_strategy_fee will raise an error if inputs are not floats."""
    params["daily_strategy_fee"] = 1
    with pytest.raises(TypeError):
         _calc_ratio_of_return(**params)

def test_bid_offer_spread_none(params):
    """Test bid_offer_spread will behave correctly when bid_offer_spread = NaN/None."""
    params["bid_offer_spread"] = nan
    with pytest.raises(TypeError):
        _calc_ratio_of_return(**params)

def test_calculate_strategy_fee_losses():
    """This module tests vectorised_calculate_strategy_fee_losses"""
    #Tests if valuerror is raised if the ratio_from_strategy_fee_losses is not float
    with pytest.raises(ValueError):
        assert vectorised._calculate_strategy_fee_losses(1, daily_strategy_fee)==1
    # Calculating the ratio_from_strategy_fee using the formula as in vectorised_calculate_strategy_fee_losses
    positions_df['ratio_from_strategy_fee']= 1 - daily_strategy_fee
    assert (
        vectorised._calculate_strategy_fee_losses(positions_df, daily_strategy_fee)
        ==positions_df['ratio_from_strategy_fee']
    )


def test_calculate_overall_ratio():
    """Tests _calculate_overall_ratio module"""
    # Calculating the ratio of returns column using the column as in _calculate_overall_ratio
    positions_df["ratio_of_return"] = (
        positions_df["raw_ratio_of_return"] * positions_df["bid_offer_loss"] * positions_df["ratio_from_strategy_fee"]
    )
    positions_df["ratio_of_return"].loc[0] = 1.0
    posistions_df['returns_key']=positions_df["ratio_of_return"].cumprod()
    assert (
        vectorised._calculate_overall_ratio(positions_df)
        ==posistions_df['returns_key']
    )

def test_clean_temporary_columns():

def test_calculate_raw_return_ratios():
    """Tests _calculate_raw_return_ratio module"""

    positions_df["raw_ratio_of_return"] = positions_df[position_key].shift(1) * positions_df[price_key]
     / positions_df[price_key].shift(1)
    ] + (1 - positions_df["yesterdays_position"])
    assert (
        vectorised._calculate_raw_return_ratio(positions_df)
        ==positions_df["raw_ratio_of_return"]
    )

def test_calculate_bid_offer_losses():
    """Tests on _calculate_bid_offer_losses module"""
    #Calculating the spread_key using given formula in vectorised._calculate_bid_offer_losses
    if isinstance(bid_offer_spread, float):
        positions_df[spread_key] = bid_offer_spread * positions_df[price_key]
    elif spread_key not in positions_df:
        print("Warning - no bid offer was supplied.")
        positions_df[spread_key] = 0.0 * positions_df[price_key]
    #Calculating yesterdays_securities using given formula in vectorised._calculate_bid_offer_losses
    positions_df["yesterdays_securities"] = (
        positions_df["yesterdays_position"] / positions_df["price_on_last_good_position"]
    )
    #Calculating todays_securities using given formula in vectorised._calculate_bid_offer_losses
    positions_df["todays_securities"] = positions_df[position_key] / positions_df[price_key]
    #Calculating the change_in_posistions using given formula in vectorised._calculate_bid_offer_lossesb and computed todays and 
    #yesterdays securities
    positions_df["change_in_positions"] = positions_df["todays_securities"] - positions_df["yesterdays_securities"]
    #Calculating the fractional_bid_offer using given formula in vectorised._calculate_bid_offer_losses 
    positions_df["fractional_bid_offer"] = positions_df[spread_key] / positions_df[price_key]
    #Calculating the bid_offer_loss using the computed metrics as inputes and formula from vectorised._calculate_bid_offer_losses
    positions_df["bid_offer_loss"] = (
        1 - abs(positions_df["change_in_positions"]) * positions_df["fractional_bid_offer"] / 2
    )

    assert (
        vectorised._calculate_bid_offer_losses(positions_df,bid_offer_spread)
        ==positions_df["bid_offer_loss"]
    )
def test_vectorised_calc_relative_bankruptcy_returns():
    """Tests _vectorised_calc_relative_bankruptcy_returns module"""
    #Calculating relative_bankruptcy_returns using the formula in vectorised._vectorised_calc_relative_bankruptcy_returns
    positions_df[returns_key][date_of_first_bankruptcy:]=positions_df["ratio_of_return"].loc[date_of_first_bankruptcy] 
    / BANKRUPTCY_SCALE_FACTOR
    positions_df["cont"]= range(0, positions_df.shape[0]) * BANKRUPTCY_TIME_PENALTY
    positions_df["portfolio_return_minus_cont"] = positions_df[returns_key] - positions_df["cont"].shift(date_of_first_bankruptcy)
    positions_df[returns_key][date_of_first_bankruptcy:] = positions_df["portfolio_return_minus_cont"][
        date_of_first_bankruptcy:
    ]
    vectorised_positions_df=positions_df.drop(["cont", "portfolio_return_minus_cont"], axis=1, inplace=True)
    
    assert (
        vectorised._vectorised_calc_relative_bankruptcy_returns(positions_df,date_of_first_bankruptcy)
        ==vectorised_positions_df
    )
    




