from decimal import *
import re

# NOTE: I just need to expand the list of SUPPORT_TYPES from the previous challenege 
# since I have designed it to accommodate all type of currency conversions.
#
# In addition, fix a bug for the rounding type. It should be ROUND_HALF_UP in most cases.

# An issue was found, so let's rename SUPPORT_TYPES to EXCHANGE_RATE and introduce CURRENCY_PREC.
# Again, EXCHANGE_RATE can be dynamically updated from the latest online information from the Internet.

#
# Here is a list of currency conversion that are supported by this program.
# In the future, the exchange rates can be dynamically updated according to online info.
#
# Format: 
#     {type of conversion} = exchange_rate
# 
# Refs:
# - Cash rounding (plz help to find a better reference): https://en.wikipedia.org/wiki/Cash_rounding
# - Python Decimal: https://docs.python.org/3/library/decimal.html
# 

EXCHANGE_RATE = {
  'USD_TO_EUR': '0.96',
  'USD_TO_JPY': '133.24819',
  'EUR_TO_USD': '1.0416667',
  'EUR_TO_JPY': '146.28332419',
  'JPY_TO_USD': '0.007507',
  'JPY_TO_EUR': '0.006828',
}

# Add extra information about the currency percision to better manage the conversion
#
# Format:
#    {currency name}: (# of digits, precision, round_type)

CURRENCY_PREC = {
  'USD': (2, '0.01', ROUND_HALF_UP),
  'EUR': (2, '0.01', ROUND_HALF_UP),
  'JPY': (0, '0',    ROUND_HALF_UP),
}

def get_rate(source, target):
    key = f'{source}_TO_{target}'
    try:
        return EXCHANGE_RATE[key]
    except KeyError:
        raise KeyError('not support conversion')


def convert(source:str, target:str, amount:str) -> Decimal:
  '''
  Convert input `amount` according to the given `convert_type`
  
  It is important the operating in floating numbers is dangerous and not precise. 
  Therefore, following strageies are used:
  - Use Decimal() to reprecent the value
  - Use quantize() to round the output according to the regulation requirements
  '''
  input_cur, output_cur = source.upper(), target.upper()
  convert_type = f'{input_cur}_TO_{output_cur}'
  input_num_digits, _, _ = CURRENCY_PREC[input_cur]
  input_pattern = r'^[+-]?\d+(\.\d{0,'+fr'{input_num_digits}'+'})?$'
  # check and convert input amount to Decimal type to start the calculation
  if not re.match(input_pattern, amount):
    raise ValueError('invalid input amount')
  input_val = Decimal(amount)
  # it is safer to calculate the amount with positive value
  output_val = input_val.copy_abs() * Decimal(EXCHANGE_RATE[convert_type])
  # put the sign back after the positive value calculation
  output_val = output_val.copy_sign(input_val)
  _, exp, round_type = CURRENCY_PREC[output_cur]
  return output_val.quantize(Decimal(exp), round_type)
