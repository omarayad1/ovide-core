#!/usr/bin/env python
from rpc_client import TestingRpcClient
from os import listdir

test_rpc = TestingRpcClient()


def compile_verilog_test():
    response = test_rpc.call('compile_verilog.compile_to_vvp("tests/batee5.v", "tests/batee5_tb.v")')
    print response
    assert eval(response) == []


def check_for_vvp_file_test():
    assert "batee5.vvp" in listdir('tests')