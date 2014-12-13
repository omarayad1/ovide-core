#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def run_vvp_file_test():
    response = test_rpc.call("vvp_utils.get_output('tests/batee5.vvp')")
    print response
    assert "F_t = 1" in eval(response)


def get_vcd_file_name_test():
    response = test_rpc.call("vvp_utils.get_vcd_filename('tests/batee5_tb.v')")
    print response
    assert response == "test.vcd"