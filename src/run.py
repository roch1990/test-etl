import asyncio
from typing import Tuple

import aiopg

import log
from clients.http_client import CoinCapHttpClient
from config import Config
from database.methods.insert import set_currency

log = log.get_logger()


async def main():

    log.info('Start downloading')

    currencies = (
        'bitcoin',
        'dogecoin',
        'dash',
        'litecoin',
        'bitcoin-cash',
        'ves',
        'zcash',
        'shitty_coin'
    )

    log.info(f'List of sources: {currencies}')

    log.info(f'Start downloading')
    data: dict = await CoinCapHttpClient.do_request(currencies)

    log.info(f'Start parsing')
    parsing_errors = []
    success_parsing = {}
    for currency, info in data.items():
        log.info(f'Start parsing for {currency}')
        await asyncio.sleep(3)
        if not info.get('data'):
            log.error(f'Parsing error for source: {currency}. Skip.')
            parsing_errors.append(currency)
            continue

        success_parsing.update({
            f"{currency}": info
        })
    log.info(f'Parse complete for resources: {success_parsing.keys()}')
    if parsing_errors:
        log.info(f'Failed parsing: {parsing_errors}')
        log.info(f'Len of failed parsings: {len(parsing_errors)}')

    log.info(f'Upload data to store: {Config.db_name}')
    try:
        engine = await aiopg.sa.create_engine(
            user=Config.db_user,
            database=Config.db_name,
            host=Config.db_host,
            password=Config.db_pass,
            port=Config.db_port
        )
    except Exception as err:
        log.error(f'DataStore connection error: {err}')
        return

    uploading_errors = []
    success_uploading = []
    for currency, info in success_parsing.items():
        try:
            await set_currency(
                engine=engine,
                currency_title=info.get('data').get('id'),
                currency_symbol=info.get('data').get('symbol'),
                currency_type=info.get('data').get('type'),
                rate_used=info.get('data').get('rateUsd'),
                timestamp=int(info.get('timestamp')),
            )
        except:
            log.error(f'Upload error for source: {currency}. Skip.')
            uploading_errors.append(currency)

    log.info(f'Upload complete for resources: {success_uploading}')
    if parsing_errors:
        log.info(f'Failed uploading: {uploading_errors}')
        log.info(f'Len of failed uploadings: {len(uploading_errors)}')
    return

asyncio.run(main())
