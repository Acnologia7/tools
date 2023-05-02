# Tools for data processing
## Reuirements:
#### Make sure to install all requirements from `requirements.txt`
## Chek residual tool
### Usage:

basic: 
- `python check_residual_tool.py <input_filepath> <--optional arg, --...>` 

optional arguments:

- `--print true` default: false
- `--chunk <int size of chunk in bytes>` default: 1024
- `--plot true`, default: false
- `--figure_size <str of x and y size(int) of axis with delimiter ','>` default='20, 20'
- `--output <output_filepath>` default: output.csv

## Dynamic terminaton tool
### Usage:

basic
- `python dynamic_termination_tool.py <input_filepath> <--optional arg, --...>`

optional arguments:
- `--residual_diff <number>` default: 0.1
- `--w_f_criterium <number>` default: 0.5
- `--sample_chunk <int>` default: 20000
