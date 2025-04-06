# Generating the SFDP

## Command line

- Prepare the environment as described in the [ASG installation instructions](./01-installing-asg.md).

- Prepare the required inputs:

    - For the source FDP, you need the FDP `url` and its openapi specification file.
    - For the new SFDP, you need the ASG instructions file and the data transformation code prepared as described [here](./03-specifying-sfdp.md).

- Select the LLM provider and its model and modify the configuration file accordingly to use the selected provider/model pair as explained in [configuration instructions](./02-configuring-asg.md). Currently, ASG supports `ollama` provider with `granite3.1-dense` and `granite-code:20b` models, see example configuration files for [`granite3.1-dense`](../examples/config/gin-ollama-local.yaml) and for [`granite-code:20b`](../examples/config/gin-ollama-tdl-node.yaml). For the `IBM WatsonX` provider with the `granite-code-inst20` model see [example configuration file](../examples/config/gin-watsonx.yaml). 

- Make sure that you are in the correct directory and in the activated virtual environment

- Execute the following command:

```sh
python src/generate_sfdp.py                     \ 
    -fdp_spec <path to FDP specification file>  \ # required
    -fdp_url <FDP URL>                          \ # required
    -fdp_timeout <seconds>                      \ # optional, default is 300
    -i <path to ASG instructions file>          \ # required 
    -t <path to data transformation code>       \ # optional, default is ./transform/ 
    -c <path to ASG configuration file>         \ # optional, default is ./config/gin-teadal-config.yaml 
    -o <path to the output directory>           \ # optional, default is ./generated_servers/
```

As a result, the directory specified as `-o` parameter will be created and will contain the new SFDP project files that can be examined and validated as decribed [here](./05-validating-sfdp.md).

## Troubleshooting

Incorrect configuration of the `GIN` library will result in error: `Reason: XXX, please make sure you have the needed configurations and access rights`. Most often, this will require assistance of the `asg` and/or the `gin` authors. Some possible causes are:

- IBM Watsonx access key is missing. Consult the [ASG configuration instructions](./02-configuring-asg.md).