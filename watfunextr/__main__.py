import argparse
from watfunextr.extractor import extract, ExtractionError
from watfunextr.parser import parse
from watfunextr.parser.parser_error import ParserError
from watfunextr.tokenizer import tokenize
from watfunextr.tokenizer.tokenizer_error import TokenizerError
from watfunextr.writer import write_from_module_fields


def main():
    parser = argparse.ArgumentParser(prog='watfunextr', description='WAT function extractor')
    parser.add_argument('module_path', metavar='module', type=str, help='The path to the WAT module')
    parser.add_argument('function', metavar='func-name-or-idx', type=str, help=f'Function to be extract')

    args = parser.parse_args()
    module_path = args.module_path

    is_idx = args.function.isdigit()
    function = args.function if not is_idx else int(args.function)

    try:
        with open(module_path, 'r') as fp:
            file_content = fp.read()
    except OSError:
        print(f'Could not open file with path: "{module_path}"')
        return

    try:
        new_module = write_from_module_fields(extract(parse(tokenize(file_content)), function))
    except (ExtractionError, ParserError, TokenizerError) as e:
        print(e)
        return
    except ValueError as e:
        print(f'Error: {str(e)}')
        return

    try:
        with open(f'function_{function}_extracted.wat', 'w') as fp:
            fp.write(new_module)
    except OSError:
        print('An error occured while writing the new WAT module')


if __name__ == "__main__":
    main()
