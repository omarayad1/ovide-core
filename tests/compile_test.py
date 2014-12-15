#!/usr/bin/env python
from rpc_client import TestingRpcClient
from os import listdir

test_rpc = TestingRpcClient()


def compile_verilog_test():
    response = test_rpc.call('compile_verilog.compile_to_vvp("batee5.v", "batee5_tb.v")')
    print response
    assert eval(response) == []