# -*- coding: utf-8 -*-
#from pytest import raises

# The parametrize function is generated, so this doesn't work:
#
#     from pytest.mark import parametrize
#
import pytest
parametrize = pytest.mark.parametrize

from bts.api import BTS
import json
from pprint import pprint


class TestMain(object):
    logfile = open("/tmp/test-bts-api.log", 'a')
    config_file = open("config.json")
    config = json.load(config_file)
    config_bts = config["bts_client"]
    config_file.close()
    client = BTS(config_bts["user"], config_bts["password"],
                 config_bts["host"], config_bts["port"])

    def test_info(self):
        result = self.client.request("get_info", []).json()["result"]
        pprint("======= test_info =========", self.logfile)
        pprint(result, self.logfile)
        assert result["blockchain_head_block_num"] > 1

    def test_asset_info(self):
        result = self.client.get_asset_info("BTS")
        assert result["symbol"] == "BTS"
        result = self.client.get_asset_info(0)
        assert result["id"] == 0
        pprint("======= test_asset_info =========", self.logfile)
        pprint(result, self.logfile)

    def test_is_asset_peg(self):
        assert self.client.is_peg_asset("CNY")
        assert not self.client.is_peg_asset("BTS")
        assert not self.client.is_peg_asset("BTSBOTS")

    def test_get_precision(self):
        assert self.client.get_precision("CNY") == 10**4
        assert self.client.get_precision("BTS") == 10**5
        assert self.client.get_precision("BTSBOTS") == 10**2

    def test_order_book(self):
        result = self.client.request("blockchain_market_order_book",
                                     ["CNY", "BTS"]).json()["result"]
        pprint("======= test_order_book =========", self.logfile)
        pprint(result, self.logfile)
        assert len(result) > 0

    def test_feed_price(self):
        feed_price_cny = self.client.get_feed_price("CNY")
        feed_price_usd = self.client.get_feed_price("USD")
        feed_price_usd_per_cny = self.client.get_feed_price("USD", base="CNY")
        assert feed_price_usd_per_cny == feed_price_usd / feed_price_cny
        assert not self.client.get_feed_price("BTSBOTS")

    def test_get_balance(self):
        balance = self.client.get_balance()
        pprint("======= test_get_balance =========", self.logfile)
        pprint(balance, self.logfile)
    #def test_publish_feeds(self):
    #def test_transfer(self):
    #def test_market_batch_update(self):
