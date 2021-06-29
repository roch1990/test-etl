import asyncio
from typing import List, Tuple

import aiohttp

from config import Config
from log import get_logger

log = get_logger()


class CoinCapHttpClient:

    @staticmethod
    async def do_request(currencies: Tuple[str]) -> dict:

        result_dict = {}
        failed_attempts = []
        success_attempts = []

        async with aiohttp.ClientSession() as session:
            for currency in currencies:
                try:
                    log.info(f'Start download {currency}')
                    await asyncio.sleep(3)
                    async with session.get(f"{Config.source_url}/{currency}") as resp:
                        result = await resp.json()

                        result_dict.update({
                            f"{currency}": result
                        })
                        success_attempts.append(currency)
                except:
                    log.error(f"Download error: {currency}")
                    failed_attempts.append(currency)

        log.info(f'Download complete for resources: {success_attempts}')
        if failed_attempts:
            log.info(f'Failed downloads: {failed_attempts}')
            log.info(f'Len of failed downloads: {len(failed_attempts)}')
        else:
            log.info(f'No failed attempts detected')

        return result_dict
