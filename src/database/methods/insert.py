from aiopg.sa import Engine
from sqlalchemy import Table

from database.models.currency import Currency


async def set_currency(
    engine: Engine,
    currency_title: str,
    currency_symbol: str,
    currency_type: str,
    rate_used: str,
    timestamp: int
):

    table: Table = Currency.__table__

    async with engine.acquire() as conn:
        async with conn.begin():

            result = await conn.execute(table.insert(
                currency_title=currency_title,
                currency_symbol=currency_symbol,
                currency_type=currency_type,
                rate_used=rate_used,
                timestamp=timestamp
            ))
    return result
