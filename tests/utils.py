def read(file_name: str) -> str:
    complete_path: str = './example_modules/' + file_name
    with open(complete_path) as f:
        return f.read()
