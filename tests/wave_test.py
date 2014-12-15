#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def check_wave_length_test():
    response = test_rpc.call("vvp_utils.get_wave('test.vcd')")
    print response
    assert len(eval(response)) > 1


def check_wave_content_test():
    response = test_rpc.call("vvp_utils.get_wave('test.vcd')")
    print response
    assert len(eval(response)["signals"]) == 3