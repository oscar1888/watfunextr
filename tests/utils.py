def read(file_name: str) -> str:
    complete_path: str = './example_modules/' + file_name
    try:
        with open(complete_path) as f:
            return f.read()
    except OSError:
        print(f'Could not open file at: {complete_path}')
