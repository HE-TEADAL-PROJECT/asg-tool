# Generating the SFDP

## Command line

- Prepare the environment as described in the [ASG installation instructions](./installing.md).

- Prepare the required inputs:

    - For the source FDP, you need the FDP `url` and its openapi specification file.
    - For the new SFDP, you need the ASG instructions file and the data transformation code prepared as described [here](./specifying-sfdp).

- Select the LLM provider and its model and modify the configuration file accordingly to use the selected provider/model. Currently, ASG supports locall `ollama` provider with the `granite3.1-dense` model (see [example configuration file](../config/gin-ollama.yaml)) and the `IBM WatsonX` provider with the `granite-code-inst20` model (see [example configuration file](../config/gin-watsonx.yaml)). More details about configuring ASG and its GIN backend are [here](./configuring-asg.md).

- When ready, execute the following command:

```sh
python src/generate_sfdp.py                     \ 
    -fdp_spec <path to FDP specification file>  \ # required
    -fdp_url <FDP URL>                          \ # required
    -i <path to ASG instructions file>          \ # required 
    -t <path to data transformation code>       \ # optional 
    -c <path to ASG configuration file>         \ # optional 
    -o <path to the output directory>           \ # optional
```

As a result, the directory specified as `-o` parameter will be created and will contain the new SFDP project files that can be examined and validated as decribed [here](./validating-sfdp.md).

## Troubleshooting

Incorrect configuration of the `GIN` library will result in error: `Reason: XXX, please make sure you have the needed configurations and access rights`. Most often, this will require assistance of the `asg` and/or the `gin` authors. Some possible causes are:

- IBM Watsonx access key is missing. Consult the [ASG configuration instructions](./configuring-asg.md).