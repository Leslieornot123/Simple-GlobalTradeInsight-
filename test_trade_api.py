import pytest
from api_integration import TradeAPI
import pandas as pd

@pytest.fixture
def trade_api():
    return TradeAPI()

def test_get_trade_data(trade_api):
    # Test with demo data
    df = trade_api.get_trade_data('842', '0', '2022')
    assert isinstance(df, pd.DataFrame)
    
def test_get_country_codes(trade_api):
    countries = trade_api.get_country_codes()
    assert isinstance(countries, dict)
    assert len(countries) > 0
    
def test_get_commodity_codes(trade_api):
    commodities = trade_api.get_commodity_codes()
    assert isinstance(commodities, dict)
    assert len(commodities) > 0
    
def test_process_trade_data(trade_api):
    # Create sample data
    df = pd.DataFrame({
        'TradeValue': ['1000', '2000', '3000'],
        'NetWeight': ['100', '200', '300'],
        'Quantity': ['10', '20', '30'],
        'Period': ['2022', '2022', '2022'],
        'TradeFlow': ['Export', 'Import', 'Export']
    })
    
    processed_df = trade_api.process_trade_data(df)
    assert isinstance(processed_df, pd.DataFrame)
    assert 'TradeBalance' in processed_df.columns
    assert processed_df['TradeValue'].dtype == 'float64' 