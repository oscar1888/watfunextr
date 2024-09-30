# watfunextr

`watfunextr` is a Python tool designed to extract a specific function from WebAssembly Text (WAT) modules along with all
its dependencies. This tool allows you to create a new "minimal" WAT module containing only the requested function,
the functions it depends on recursively and some other dependencies.

## Features

- Extract a specified function from a WebAssembly Text (.wat) module
- Include all dependent functions recursively in the new WAT module
- Assist in debugging and isolating specific parts of WebAssembly Text modules

## Requirements
- Python 3.10 or higher

## Installation
You can install `watfunextr` by cloning this repository and installing the required dependencies:
```bash
git clone https://github.com/oscar1888/watfunextr.git
cd watfunextr
pip install -r requirements.txt
```

## Usage
### Extracting a Function

To extract a specific function from a WAT module, use the following command:
```bash
python3 -m watfunextr <path-to-wasm-file> <function-name-or-index>
```

For example:
```bash
python3 -m watfunextr tests/operations.wasm $add
```
or:
```bash
python3 -m watfunextr tests/operations.wasm 2
```

This will create a new WAT module containing only the `$add` function and all functions it depends on (with some other
dependencies).

### Output

The tool will output a new WAT file named `function_<function-name-or-index>_extracted.wat` in the current directory,
containing only the requested function and its dependencies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
