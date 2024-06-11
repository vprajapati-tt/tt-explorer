#include "mlir/IR/MLIRContext.h"
#include "mlir/InitAllDialects.h"
#include "mlir/InitAllPasses.h"
#include "mlir/Pass/PassManager.h"
#include "mlir/Support/FileUtilities.h"
#include "mlir/Tools/mlir-opt/MlirOptMain.h"

#include "Passes.h.inc"
#include "IR/TTIROpsDialect.h.inc"
#include "IR/TTKernelOpsDialect.h.inc"
#include "IR/TTOpsDialect.h.inc"

#include <string>
#include <pybind11/pybind11.h>
// Now insert the code to transform from the MLIR Dialect to a parsed JSON or smth idk


PYBIND11_MODULE(tt_adapter, m) {
    m.doc() = "TT-Adapter Module to bind from C++ MLIR Bindings to Python";

    m.def("initialize", []() -> void {
        mlir::registerAllPasses();
    }, "Initialize passes and dialects for MLIR");
    m.def("add", [](int a, int b) -> int {return a + b;}, "add 2 numbers");
    m.def("generateJSON", []() -> std::string {return "hi";}, "Generate the Model Builder JSON File");
}