# Distribution Estimator

This tool finds the distribution that best fits an input dataset.

## Requirements

To be able to use this tool, you need to have `python` installed with at least version `3.9`.
To install the required dependencies, run the following command:

```
[pip command] install -r requirements.txt
```

where `[pip command]` is replaced with `pip3` if you are working on a Unix/Linux based system or with `pip` if you are working on a Windows system.

## Run

To use the tool, run the following command:

```
[python command] -m src.estimation_tool [input file path]
```

where `[python command]` is replaced with `python3` if you are working on a Unix/Linux based system or with `python` if you are working on a Windows system and `[input file path]` is replaced with the path to the file containing non-negative integer values with each value contained in a separate line.

To try the existing sample, run:
```use
[python command] -m src.estimation_tool example_sample.txt
```

which will output:
```
Best discrete distribution fit result:
Zipfian(s = 0.8742652627639053, n = 3)
according to the test: Chi-Square Test
statistic: 0.0885003158140516
p-value: 0.9567145978140291
No suitable continuous distribution was found for the given data.
```

## Development

The functional part of the code is contained in the `src` directory. All unit tests are found in the `test` directory. 

To run the unit tests, execute the script `run_tests.sh`.