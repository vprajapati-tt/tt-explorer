# TT-Explorer
TT-Explorer is a development tool to better visualize, modify, and optimize compiled TT-MLIR Graphs.

## Structure
The structure of the TT-Explorer project follows what is below, and is dependant on the following projects as well:

### [TT-MLIR](https://github.com/tenstorrent/tt-mlir)
TT-MLIR is the "middle-out" compiler that allows for some visualizer tool to seamlessly integrate into the compilation process to allow for user driven (read: Human-In-Loop) overrides and optimizations. The project is built using the Python bindings generated out of TT-MLIR to parse, modify, and run models.

### [Model Explorer](https://github.com/google-ai-edge/model-explorer)
Model Explorer is currently used as the tool to visualize MLIR models being generated. Currently the main issue with model-explorer is that the frontend is not yet open sourced. Model-explorer provides an extensible adapter interface, where these custom adapters emit JSON Graphs to be parsed by the model-explorer visualizer and displayed. Model Explorer also contains the functionality to display "Node Data", which can allow for simple performance overlays.

### [TT-Adapter](https://github.com/vprajapati-tt/tt-adapter)
Building on top of model explorer's adapter framework, TT-Adapter is a specific adapter made for TT-MLIR dialects such that the emitted MLIR can be parsed and displayed using the model-explorer visualizer tool.

### TT-Explorer
TT-Explorer serves as an endpoint for users and developers to access these Human-In-Loop compiler overrides, it packages the adapter and model-explorer tools together, while adding additional functionality for endpoints like Jupyter Notebooks, REST APIs, and a python package. TT-Explorer also serves as a platform to prototype and develop front-end additions that would allow for TT-Specific visualizations (ex: Core Grids, etc...)

## Desired Outcome
The endgoal for the tool is to be able to easily process overrides on Op Attributes, be able to visualize the result of this override, and iteratively continue that process. In terms of the current tech stack that looks like:
TT-MLIR (representation) -> TT-Explorer -> Model Explorer + Overrides Config -> modify MLIR Module -> Execute Modified MLIR Module (ttrt) -> Visualize Perf Trace (Model-Explorer Node Data) -> Step 1

### Overrides
Overrides are *currently* defined as the method with which attributes of operations can be overriden using TT-Explorer. This could mean changing the memory space that a tensor is compiled to remain in (ex: from DRAM -> L1) or modifications of the core grid with which that operation is planned to execute on.

Overrides are currently defined as JSON, keyed with a UID of an operation and valued with a dictionary of attributes and the new value of that attribute.

## Progress / Research Goals
- [ ] `TT-MLIR` Flesh out and develop `overrides` in the `ttmlir` dialect Python Binding to allow for JSON overrides
- [ ] `TT-Explorer` Research front end changes to allow for easy grid visualization of each Op
- [ ] `TT-Explorer` Implement overrides method in API, potentially integrate an "options" generation for valid entries that would fit the attribute.

## Installation
1. Build TT-MLIR
2. Activate TT-MLIR venv
3. pip install . in TT-Adapter
4. pip install . in TT-Explorer
5. Test in either Notebook API or by running tt-explorer in Shell

## How to use
TT-Explorer is built with Google's Model Explorer as a visual backbone, and powered with Python and HTTP API endpoints. Users can use the `notebook.ipynb` file to familiarize themselves with the Python endpoints for rapid development in the Notebook format. Users can also run `tt-explorer` to get a sense for a simple web-app UI that allows for quick exploration and modification of a TT-Graph.

## API Reference
