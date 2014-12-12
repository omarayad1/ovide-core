#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def out_test():
    response = test_rpc.call("tests/batee5.v")
    print response
    assert response.find('tests/batee5.v:8: Delayed assignments (<=) '
                         'in non-clocked (non flop or latch) block; '
                         'suggest blocking assignments (=).') + 1


def out_test_fixed():
    response = test_rpc.call("tests/batee5_fixed.v")
    print response
    assert response == ''
