def parse_int(string: str) -> int | None:
    try:
        return int(string)
    except ValueError:
        return None


def parse_sample_file(sample_file: str) -> list[int]:
    with open(sample_file, 'r') as f:
        return list(filter(lambda x: x is not None,
                           map(lambda x: parse_int(x.strip()),
                               f.readlines())))
