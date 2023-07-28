from database.models import Cryptocurrency


def get_slug_names_from_cryptocurrencies(s):
    slug_names = [slug_name[0]
                  for slug_name
                  in s.query(Cryptocurrency.slug_name).distinct().all()]

    return slug_names


def get_market_id_and_contracts_from_cryptocurrencies(s):
    contracts_with_id = s.query(Cryptocurrency.marketcap_id, Cryptocurrency.contracts).all()

    return [i for i in contracts_with_id if i[1]]
