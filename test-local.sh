git submodule update

cd third_party/tt-mlir
make

cd ../../tt-adapter
pip install -e .

model-explorer --extensions=tt_adapter