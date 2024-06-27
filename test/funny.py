# RUN: %python %s | FileCheck %s

from ttmlir.ir import *
from ttmlir.dialects import ttkernel, ttir, tt

f = open("tosa-to-ttir.ttir", "r")
fs = "".join(f.readlines())

with Context() as ctx:
    ttkernel.register_dialect(ctx)
    ttir.register_dialect(ctx)
    tt.register_dialect(ctx)
    module = Module.parse(fs, ctx)

    # CHECK: %[[C:.*]] = arith.constant 2 : i32
    # CHECK: ttmlir.foo %[[C]] : i32
