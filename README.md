# wafunextr

`wafunextr` is a Python tool designed to extract a specific function from WebAssembly (WASM) modules along with all its dependencies. This tool allows you to create a new "minimal" WASM module containing only the requested function and the functions it depends on recursively.

## Features

- Extract a specified function from a WebAssembly (.wasm) module
- Include all dependent functions recursively in the new WASM module
- Assist in debugging and isolating specific parts of WebAssembly modules

## Requirements
- Python 3.10 or higher
- `wasm2wat` module to convert WASM files to WAT (WebAssembly Text format)
- `wat2wasm` module to convert WAT files back to WASM

## Installation
You can install `wafunextr` by cloning this repository and installing the required dependencies:
```bash
git clone https://github.com/oscar1888/wafunextr.git
cd wafunextr
pip install -r requirements.txt
```

## Usage
### Extracting a Function

To extract a specific function from a WASM module, use the following command:
```bash
python3 -m wafunextr <path-to-wasm-file> <function-name>
```

For example:
```bash
python3 -m wafunextr tests/operations.wasm add
```

This will create a new WASM module containing only the `add` function and all functions it depends on.

### Example Output

The tool will output a new WASM file named `<function-name>_extracted.wasm` in the current directory, containing only the requested function and its dependencies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
