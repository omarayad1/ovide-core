#!/usr/bin/env python
from rpc_client import TestingRpcClient

test_rpc = TestingRpcClient()


def content_test():
    response = test_rpc.call("generate_testbench.generate_testbench('batee5.v')")
    print len(response)
    assert len(response) == 353