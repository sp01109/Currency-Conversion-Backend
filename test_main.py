import pytest, sys
from decimal import Decimal
from httpx import AsyncClient

from main import app


@pytest.fixture
def anyio_backend():
    # only run the test with asyncio module
    return 'asyncio'


@pytest.mark.parametrize("source,target", [('usd','jpy'),('usd','eur'),('jpy','usd'),('jpy','eur'),('eur','usd'),('eur','jpy')])
@pytest.mark.anyio
async def test_get_exchange_rate(source:str, target:str):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/exchange_rate/{source}/{target}")
    assert response.status_code == 200
    output = response.json()
    assert 'source_currency' in output
    assert 'target_currency' in output
    assert 'exchange_rate' in output
    assert 'source_precision' in output


test_data = [
  # [2 decimal to 2 decimal] (i.e. USD_TO_EUR, EUR_TO_USD)   
  # cases of very basic cases 
  ("USD", "EUR", "0.00", "0.00"),    
  ("USD", "EUR", "0", "0.00"),    
  ("USD", "EUR", "+0", "0.00"),   
  ("USD", "EUR", "-0", "0.00"),  
  ("USD", "EUR", "1", "0.96"),   
  ("USD", "EUR", "1.0", "0.96"),   
  ("USD", "EUR", "1.00", "0.96"),    
  ("USD", "EUR", "+1", "0.96"),   
  ("USD", "EUR", "+1.", "0.96"),   
  ("USD", "EUR", "+1.0", "0.96"),   
  ("USD", "EUR", "+1.00", "0.96"),   
  ("USD", "EUR", "-1", "-0.96"),   
  ("USD", "EUR", "-1.", "-0.96"),  
  ("USD", "EUR", "-1.0", "-0.96"), 
  ("USD", "EUR", "-1.00", "-0.96"),   
  # normal cases 
  ("USD", "EUR", "0.01", "0.01"),  
  ("USD", "EUR", "0.10", "0.10"),       
  ("USD", "EUR", "0.12", "0.12"), 
  ("USD", "EUR", "0.50", "0.48"),    
  ("USD", "EUR", "0.99", "0.95"), 
  ("USD", "EUR", "1.50", "1.44"),      
  ("USD", "EUR", "2.50", "2.40"),    
  ("USD", "EUR", "5.55", "5.33"), 
  ("USD", "EUR", "10.75", "10.32"),  
  ("USD", "EUR", "12.35", "11.86"), 
  ("USD", "EUR", "100", "96.00"),
  # some large numbers
  ("USD", "EUR", "1000", "960.00"),
  ("USD", "EUR", "9999", "9599.04"),
  ("USD", "EUR", "10000", "9600.00"),
  ("USD", "EUR", "1000000000", "960000000.00"),
  # numbers that exceed `sys.maxsize`
  ("USD", "EUR", f"{sys.maxsize}", "8854437155380584774.72"),
  ("USD", "EUR", f"{sys.maxsize}0", "88544371553805847747.20"),
  # negative normal values
  ("USD", "EUR", "-0.12", "-0.12"), 
  ("USD", "EUR", "-0.50", "-0.48"),    
  ("USD", "EUR", "-0.99", "-0.95"),
  ("USD", "EUR", "-1.00", "-0.96"),   
  ("USD", "EUR", "-1.50", "-1.44"),      
  ("USD", "EUR", "-2.50", "-2.40"),    
  ("USD", "EUR", "-5.55", "-5.33"), 
  ("USD", "EUR", "-10.75", "-10.32"),  
  ("USD", "EUR", "-12.35", "-11.86"), 
  # negative numbers that exceed -`sys.maxsize`
  ("USD", "EUR", f"-{sys.maxsize}", "-8854437155380584774.72"),
  ("USD", "EUR", f"-{sys.maxsize}0", "-88544371553805847747.20"),
  # 
  # [2 decimal to 0 decimal]  (i.e. USD_TO_JPY, EUR_TO_JPY)
  #
  # cases of very basic cases 
  ("USD", "JPY", "0.00", "0"),
  ("USD", "JPY", "0", "0"),    
  ("USD", "JPY", "+0", "0"),   
  ("USD", "JPY", "-0", "0"),  
  ("USD", "JPY", "1", "133"),   
  ("USD", "JPY", "1.0", "133"),   
  ("USD", "JPY", "1.00", "133"),    
  ("USD", "JPY", "+1", "133"),   
  ("USD", "JPY", "+1.", "133"),   
  ("USD", "JPY", "+1.0", "133"),   
  ("USD", "JPY", "+1.00", "133"),   
  ("USD", "JPY", "-1", "-133"),   
  ("USD", "JPY", "-1.", "-133"),  
  ("USD", "JPY", "-1.0", "-133"), 
  ("USD", "JPY", "-1.00", "-133"),   
  # normal cases 
  ("USD", "JPY", "0.01", "1"),
  ("USD", "JPY", "0.10", "13"),
  ("USD", "JPY", "0.12", "16"),
  ("USD", "JPY", "0.50", "67"),
  ("USD", "JPY", "0.99", "132"),
  ("USD", "JPY", "1.50", "200"),
  ("USD", "JPY", "2.50", "333"),
  ("USD", "JPY", "5.55", "740"),
  ("USD", "JPY", "10.75", "1432"),
  ("USD", "JPY", "12.35", "1646"),
  ("USD", "JPY", "100", "13325"),
  # some large numbers
  ("USD", "JPY", "1000", "133248"),
  ("USD", "JPY", "9999", "1332349"),
  ("USD", "JPY", "10000", "1332482"),
  ("USD", "JPY", "1000000000", "133248190000"),
  # numbers that exceed `sys.maxsize`
  ("USD", "JPY", f"{sys.maxsize}", "1228997629607512169139"),
  ("USD", "JPY", f"{sys.maxsize}0", "12289976296075121691385"),
  # negative normal values
  ("USD", "JPY", "-0.12", "-16"),    
  ("USD", "JPY", "-0.50", "-67"),    
  ("USD", "JPY", "-0.99", "-132"),    
  ("USD", "JPY", "-1.00", "-133"),    
  ("USD", "JPY", "-1.50", "-200"),    
  ("USD", "JPY", "-2.50", "-333"),    
  ("USD", "JPY", "-5.55", "-740"),    
  ("USD", "JPY", "-10.75", "-1432"),
  ("USD", "JPY", "-12.35", "-1646"),
  # negative numbers that exceed -`sys.maxsize`
  ("USD", "JPY", f"-{sys.maxsize}", "-1228997629607512169139"),
  ("USD", "JPY", f"-{sys.maxsize}0", "-12289976296075121691385"),
  #
  # [0 decimal to 2 decimal] (i.e. JPY_TO_EUR, JPY_TO_USD)
  #
  ("JPY", "EUR", "0", "0.00"), 
  ("JPY", "EUR", "+0", "0.00"),   
  ("JPY", "EUR", "-0", "0.00"),  
  ("JPY", "EUR", "1", "0.01"),       
  ("JPY", "EUR", "+1", "0.01"),   
  ("JPY", "EUR", "+1.", "0.01"),   
  ("JPY", "EUR", "-1", "-0.01"),   
  ("JPY", "EUR", "-1.", "-0.01"),   
  # normal cases 
  ("JPY", "EUR", "2", "0.01"),
  ("JPY", "EUR", "3", "0.02"),    
  ("JPY", "EUR", "5", "0.03"),    
  ("JPY", "EUR", "10", "0.07"),    
  ("JPY", "EUR", "11", "0.08"),    
  ("JPY", "EUR", "12", "0.08"),    
  ("JPY", "EUR", "100", "0.68"),
  # some large numbers
  ("JPY", "EUR", "1000", "6.83"),
  ("JPY", "EUR", "9999", "68.27"),
  ("JPY", "EUR", "10000", "68.28"),
  ("JPY", "EUR", "1000000000", "6828000.00"),
  # numbers that exceed `sys.maxsize`
  ("JPY", "EUR", f"{sys.maxsize}", "62977184267644409.21"),
  ("JPY", "EUR", f"{sys.maxsize}0", "629771842676444092.10"),
  # negative normal values
  ("JPY", "EUR", "-2", "-0.01"),
  ("JPY", "EUR", "-3", "-0.02"),    
  ("JPY", "EUR", "-5", "-0.03"),    
  ("JPY", "EUR", "-10", "-0.07"),    
  ("JPY", "EUR", "-11", "-0.08"),    
  ("JPY", "EUR", "-12", "-0.08"),    
  ("JPY", "EUR", "-100", "-0.68"),
  # negative numbers that exceed -`sys.maxsize`
  ("JPY", "EUR", f"-{sys.maxsize}", "-62977184267644409.21"),
  ("JPY", "EUR", f"-{sys.maxsize}0", "-629771842676444092.10"),
]


@pytest.mark.parametrize("source,target,amount,expected", test_data)
@pytest.mark.anyio
async def test_convert_currency(source:str, target:str, amount:str, expected:str):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/convert/{source}/{target}?amount={amount}")
    assert response.status_code == 200
    output = response.json()
    assert 'source_currency' in output
    assert 'source_amount' in output
    assert 'target_currency' in output
    assert 'target_amount' in output
    assert 'exchange_rate' in output
    assert Decimal(output['target_amount']) == Decimal(expected)


