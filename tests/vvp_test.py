#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def run_vvp_file_test():
    response = test_rpc.call("vvp_utils.get_output('batee5.vvp')")
    print response
    assert "F_t = 1" in eval(response)