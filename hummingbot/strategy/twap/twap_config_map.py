from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_validators import (
    validate_exchange,
    validate_market_trading_pair,
)
from hummingbot.client.settings import (
    required_exchanges,
    EXAMPLE_PAIRS,
)
from typing import Optional


def trading_pair_prompt():
    exchange = twap_config_map.get("exchange").value
    example = EXAMPLE_PAIRS.get(exchange)
    return "Enter the token trading pair you would like to trade on %s%s >>> " \
           % (exchange, f" (e.g. {example})" if example else "")


def target_asset_amount_prompt():
    trading_pair = twap_config_map.get("trading_pair").value
    base_token, _ = trading_pair.split("-")

    return f"What is the total amount of {base_token} to be traded? (Default is 1.0) >>> "


def str2bool(value: str):
    return str(value).lower() in ("yes", "y", "true", "t", "1")


# checks if the trading pair is valid
def validate_market_trading_pair_tuple(value: str) -> Optional[str]:
    exchange = twap_config_map.get("exchange").value
    return validate_market_trading_pair(exchange, value)


twap_config_map = {
    "strategy":
        ConfigVar(key="strategy",
                  prompt=None,
                  default="twap"),
    "exchange":
        ConfigVar(key="exchange",
                  prompt="Enter the name of the exchange >>> ",
                  validator=validate_exchange,
                  on_validated=lambda value: required_exchanges.append(value),
                  prompt_on_new=True),
    "trading_pair":
        ConfigVar(key="trading_pair",
                  prompt=trading_pair_prompt,
                  validator=validate_market_trading_pair_tuple,
                  prompt_on_new=True),
    "trade_side":
        ConfigVar(key="trade_side",
                  prompt="What operation will be executed? (buy/sell) >>> ",
                  type_str="str",
                  validator=lambda v: None if v in {"buy", "sell", ""} else "Invalid operation type.",
                  default="buy",
                  prompt_on_new=True),
    "target_asset_amount":
        ConfigVar(key="target_asset_amount",
                  prompt=target_asset_amount_prompt,
                  default=1.0,
                  type_str="decimal",
                  prompt_on_new=True),
    "order_step_size":
        ConfigVar(key="order_step_size",
                  prompt="What is the amount of each individual order (denominated in the base asset, default is 1)? "
                         ">>> ",
                  default=1.0,
                  type_str="decimal",
                  prompt_on_new=True),
    "order_price":
        ConfigVar(key="order_price",
                  prompt="What is the price for the limit orders? >>> ",
                  type_str="decimal",
                  prompt_on_new=True),
    "order_delay_time":
        ConfigVar(key="order_delay_time",
                  prompt="How many seconds do you want to wait between each individual order?"
                         " (Enter 10 to indicate 10 seconds. Default is 10)? >>> ",
                  type_str="float",
                  default=10,
                  prompt_on_new=True),
    "cancel_order_wait_time":
        ConfigVar(key="cancel_order_wait_time",
                  prompt="How long do you want to wait before cancelling your limit order (in seconds). "
                         "(Default is 60 seconds) ? >>> ",
                  type_str="float",
                  default=60,
                  prompt_on_new=True)
}