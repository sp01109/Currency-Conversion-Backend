from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import convert, get_rate, CURRENCY_PREC


'''
#
# NOTE: Source of `utils.EXCHANGE_RATE` is just an example here.
#
# In the actual production, here are several solutions with pros/cons. Solution C will mostly the best solution as deploying this application.
#
# [Solution A] Database with event-driven update
# 
# This solution maintains an database (such as using AWS RDS) and update the exchange rate info 
# regularly by using the serverless, event-driven server like AWS Lambda.
# 
# Pros: 
# - reducing 3rd-party source inquery, which reduce the cost
# - can refer to mutiple sources to ensure the 'reliability' and 'accurateness'
# - higher response speed from our API
#
# Cons:
# - Extra work on setting up and monitoring the information updated in the database
# - Need to figuring out correct time to inquery the update from 3rd-party source
#
#
# [Solution B] Always get exchange rate from 3rd party source
#
# This solution will always request the latest exchange rate from 3rd party source everytime our API is called.
# 
# Pros:
# - ensure always getting the latest rate
# 
# Cons:
# - could reduce the response time because of waiting the response from the external API call
# - much more cost because high demand to the 3rd party source
# - not easy to ensure the accuracy by refering to mutiple sources
# - low reliability becuase relying on single source
#
#
# [Solution C] Use cache service (like Redis) to cache the exchange rate info with time-to-live (TTL) setup.
#
# This combines the benefits of Solution A and Solution B. 
# The exchange rate will only be queried from the 3rd part source when there is a call to our API. 
# The rate will be kept in cache service based on the trusted time-to-live (TTL) lifespan. 
# Such info in the cache service will be reused in the following up API calls if the content is still alive.
# 
# Pros:
# - query to 3rd part source as-needed
# - less work on maintaining our exchange rate info because of TTL setup
# - easiler to setup a cache service than a database service with Lambda service
# - balanced response speed because of reducing time in querying to either database or 3rd-party source
# - balanced cost since it avoid redudent inquiry to maintain our database
#
# Cons:
# - not really having disadvantage
# 
'''


class ExchangeRate(BaseModel):
    source_currency: str
    target_currency: str
    exchange_rate: str
    source_precision: int

    
class CurrencyConversionResult(BaseModel):
    source_currency: str
    source_amount: str
    target_currency: str
    target_amount: str
    exchange_rate: str


app = FastAPI()


@app.get("/exchange_rate/{source_currency}/{target_currency}")
async def exchange_rate(source_currency: str, target_currency:str):
    """
    Retrieves the exchange rate from the source currency to the target currency.

    :param source_currency: The currency to exchange from.
    :param target_currency: The currency to exchange to.

    :return: The exchange rate information in `ExchangeRate`.
    """
    source = source_currency.upper()
    target = target_currency.upper()
    try:
        exchange_rate = get_rate(source, target)
        source_precision = CURRENCY_PREC[source][0]
    except KeyError:
        msg = f"Does not support conversion from {source} to {target}"
        raise HTTPException(status_code=404, detail=msg)
    return ExchangeRate(
            source_currency=source, 
            target_currency=target, 
            exchange_rate=exchange_rate, 
            source_precision=source_precision
        )



@app.get("/convert/{source_currency}/{target_currency}")
async def convert_currency(source_currency: str, target_currency:str, amount:str = "1"):
    """
    Converts an amount from the source currency to the target currency.

    :param source_currency: The currency to convert from.
    :param target_currency: The currency to convert to.
    :param amount: The amount to convert. (Optional, Default: 1)
    
    :return: The converted result in `CurrencyConversionResult`.
    """
    # trim the possible white-spaces
    amount = amount.strip()
    source = source_currency.upper()
    target = target_currency.upper()
    try:
        exchange_rate = get_rate(source, target)
        target_amount = convert(source, target, amount)
    except KeyError:
        msg = f"Does not support conversion from {source} to {target}"
        raise HTTPException(status_code=404, detail=msg)
    except ValueError:
        source_precision = CURRENCY_PREC[source][0]
        msg = f"Invalid input amount: {amount}. (precision: {source_precision} decimal digits)"
        raise HTTPException(status_code=400, detail=msg)
    
    return CurrencyConversionResult(
                source_currency = source,
                source_amount = amount,
                target_currency = target,
                target_amount = str(target_amount),
                exchange_rate = str(exchange_rate),
            )
