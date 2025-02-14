def sorted_output(output: dict|set) -> list:
    if isinstance(output, set):
        return sorted(output)
    elif isinstance(output, dict):
        return sorted(output.items(), key=lambda item: item[0])
    else:
        raise TypeError
