from steampy.client import SteamClient, Asset
from steampy.utils import GameOptions, get_key_value_from_url, account_id_to_steam_id

steam_client = SteamClient('3B24111B3C934BD1FED5873AF3664560')
steam_client.login('pass', 'name', 'steamguard.json')



def find_item_in_inventory(item_hash_name, items):
    for item in items.values():
        market_hash_name = item['market_hash_name']
        if market_hash_name != item_hash_name:
            continue
        return {
            'market_hash_name': market_hash_name,
            'id': item['id']
        }


def make_trade_1_item(give_item, get_item, trade_link):
    game = GameOptions.TF2
    my_items = steam_client.get_my_inventory(game)
    my_item_give = find_item_in_inventory(give_item, my_items)
    my_asset = [Asset(my_item_give['id'], game)]

    partner_account_id = get_key_value_from_url(trade_link, 'partner', True)
    partner_steam_id = account_id_to_steam_id(partner_account_id)
    partner_items = steam_client.get_partner_inventory(partner_steam_id, game)

    steam_client.make_offer_with_url(my_asset, [], trade_link, '1337')


