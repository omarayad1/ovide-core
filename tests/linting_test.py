#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def out_test():
    response = test_rpc.call("lint_verilog.check_for_errors('batee5.v')")
    print response
    assert eval(response)[0]["line"] == 8


def out_test_fixed():
    response = test_rpc.call("lint_verilog.check_for_errors('batee5_fixed.v')")
    print response
    assert eval(response) == []
