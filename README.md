# ml-ethereum-fraud
A comparative analysis of dataset characteristics and their impact in ML performance


# TL; DR

Read the dataset setup to put the data files required where they belong and run:

```sh
./scripts/install-env.sh
source .venv/bin/activate
python src/experiments/showcase.py
```



## Installation

### Virtual environment

Run the following command:

```sh
chmod +x scripts/install-env.sh
./scripts/install-env.sh
```

## Configuration

The configuration of the project is handled using the `params.yaml` file. It is recommended to add new information there if required and not hardcoding any values in the code.

## Data

Datasets need to be placed in the `data` directory under the appropiate name. For example, for the dataset in which both ends of the edges belong to the ground truth data, an edge file and a node file need to be placed in the `data` folder under the names: `both_ends_belong_edges.csv` and `both_ends_belong_nodes.csv`.

The exact filename exacted for each dataset can be found inside the `src/datasets/variations/` folder.

## Running the experiments

All experiments are located inside the `src/experiments/` folder. We offer an experiment titled `showcase.py` that can be used as a guide on how to build new experiments.