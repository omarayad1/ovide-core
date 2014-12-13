#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def check_wave_length_test():
    response = test_rpc.call("wave_utils.get_wave('test.vcd')")
    print response
    assert len(eval(response)) > 1


def check_wave_content_test():
    response = test_rpc.call("wave_utils.get_wave('test.vcd')")
    print response
    assert eval(response)["signals"][0]["wave"] == [[0, '1'], [3000, '0']]