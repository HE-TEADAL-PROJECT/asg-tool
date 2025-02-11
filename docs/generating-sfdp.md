# Generating the SFDP

## Command line

- Prepare the environment as described in [installation instructions](./installing.md)

- Prepare the required inputs:

    - For the source FDP, the `url` and the openapi specification file
    - For the new SFDP, the ASG instructions file and data transformation code prepared as described [here](./specifying-sfdp)

- Configure the LLM provider and model and modify the configuration file accordingly to the selected provider. Currently, `asg` supports locall `ollama` with the `granite3.1-dense` model (see [example configuration file](../config/gin-ollama.yaml)) and the `IBM WatsonX` with the `granite-code-inst20` model (see [example configuration file](../config/gin-watsonx.yaml)).

- When ready, execute the following command:

```sh
python src/generate_sfdp.py 
    -fdp_spec <path to FDP specification file> # required
    -fdp_url <FDP URL>                         # required
    -i <path to ASG instructions file>         # required 
    -t <path to data transformation code>      # optional 
    -c <path to ASG configuration file>        # optional 
    -o <path to the output directory>          # optional
```

As a result, the directory specified as `-o` parameter will be created and will contain the new SFDP files that can be examined and validated as decribed [here](./validating-sfdp.md).

## Troubleshooting

- Incorrect configuration of the IBM Watsonx access will result in error: `Reason: XXX, please make sure you have the needed configurations and access rights`. Most often, this will require assistance of the `asg` and/or the `gin` authors.