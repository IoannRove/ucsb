async def update_currencies(redis, merge: int, currencies: dict):
    """
    Добавление значений валют в redis.
    """
    if merge:
        await redis.hmset_dict('currencies', currencies)
    else:
        await redis.delete('currencies')
        await redis.hmset_dict('currencies', currencies)
