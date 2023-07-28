def get_pages(market_id):
    if market_id <= 500:
        return 10

    if 500 <= market_id <= 2500:
        return 5

    if 2500 <= market_id:
        return 3



