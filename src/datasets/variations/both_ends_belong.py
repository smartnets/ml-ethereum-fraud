"""
We expect two files:

`data/both_ends_belong_edges.csv`
`data/both_ends_belong_nodes.csv`

"""


def parse_edge(line):
    parts = line.strip().split(",")

    from_ = parts[1]
    to_ = parts[3]

    features = {
        "amount": int(parts[5]),
        "time": parts[6],
        "block_number": int(parts[7]),
    }
    return from_, to_, features


def parse_node(line):
    parts = line.strip().split(",")

    addr = parts[0]

    features = {
        "isECR": float(bool(parts[1])),
        "isMiner": float(bool(parts[-1])),
        "fradulent": parts[-2] == "Dodgy",
    }
    return addr, features
