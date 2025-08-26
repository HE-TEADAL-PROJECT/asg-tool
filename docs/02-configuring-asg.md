# Configuring the ASG-Tool

ASG-Tool depends on IBM Gin library that implements the agentic system for generating data connectors. IBM GIN Library employs Large Language Models (LLMs) to perform generative AI tasks. For the system to work, it must have access to a supported LLM provider and a supported model that this provider can execute. Thus, ASG-Tool requires a configutation file to be passed to the GIN library at runtime. This configuration file is a `yaml` file with the entries described below. ASG tool accepts the path to the configuration file as a parameter, default path is `./config/gin-teadal-config.yaml`.

## `aiPlatforms` entry
This entry specifies the list of LLM Providers that can be used, selected by what's specified later in the file in the `generation` entry.
Currently, IBM GIN library supports several LLM providers. For TEADAL project, the possibilities are:

1. `ollama` requires `ollama` server to be accessible. The server can be installed either on the developer's workstation where the ASG is run or on a server accessible from the developer's workstation. In any case, the address of the `ollama` server has to be configured. For reference, see examples for the [ollama service running locally](../examples/config/gin-ollama-local.yaml) and for the [ollama service running on TEADAL Node](../examples/config/gin-ollama-tdl-node.yaml). 
> **Note**
> Above files are provided as examples. You need to edit the `api_base` entry to suite your installation of Ollama service.

To check accessibility of Ollama service, you can, for example, invoke:
```sh
$ curl <Ollama service IP>/ollama/api/tags | python -m json.tool
```

2. `IBM WatsonX` provider is available through the IBM Cloud as a service. To use this provider, one must be registered with the IBM cloud and obtain the API key and the projectID as shown in the [ASG-watsonx configuration example](../examples/config/gin-watsonx.yaml). 

## `models` entry
This entry specifies the list of models that can be used, selected by what's specified later in the file in the `generation` entry.
Developers of the IBM GIN Library work to validate and select the best models for each supported task. For the TEADAL SFDP generation, we advise using the selected and tested models that are listed in the example configuration files:

1. `ollama` provider shall be used with the `granite3.1-dense` models family. 
2. `IBM WatsonX` provider shall be used with the `granite-code-inst20` models family.

## `generation` entry
This entry specifies one specific model to be executed in the current run, referencing one of the models listed in the `models` entry of the configuration file. In addition, it is possible to specify:

- The maximum number of retries allowed for the model to process a user query if static checks identify issues in the LLM's response as `maxIter`.
- The features enabled as part of GIN execution as `features`. Possible settings are:
    - **rag**: enables or disables the Retrieval-Augmented Generation feature.
    - **staticChecks**: conducts static checks to identify syntactic issues based on the context and the LLM's response.
    - **llmEval**: provides LLM evaluation of the response (currently not supported).

## Example

```yaml
# list of the available platforms
aiPlatforms:    
  # ollama - only requires the server URL
  OLLAMA:       
    platform: openai
    credentials:
      api_key: ollama
      # EDIT THIS URL TO SUITE YOUR OLLAMA INSTALLATION!!!
      api_base: http://localhost:11434/v1 
  # watsonx - required the URL (do not change), API key (use yours), and project id (use yours)
  Watsonx:      
    platform: watsonx
    credentials:
      api_key: <use yours>
      api_base: https://us-south.ml.cloud.ibm.com
      api_project_id: <use yours>

# list of the models supported by GIN and 
# available on one of the providers listed above
# along with their parameters
models:     
  granite-code-inst20:
    id: ibm/granite-20b-code-instruct
    host: Watsonx
    parameters:
      decoding_method: greedy
      max_new_tokens: 1024
      random_seed: 10
      temperature: 0
  granite3.1-dense:
    id: granite3.1-dense:2b
    host: OLLAMA
    parameters:
      max_tokens: 1024
      seed: 10
      temperature: 0

# model and features currently selected from the list above 
# to be used for SFDP generation
generation:  
  models:
    - granite-code-inst20
  maxIter: 3
  features:
    rag: false
    staticChecks: true
    llmEval: false
```

## Proceed generating the SFDP 

Now when you have installed and configured the ASG-Tool, you can proceed with the following steps:
- Prepare ASG-Tool inputs to suite the requirements of your FDP-to-SFDP contract following the [sFDP specification instructions](./03-specifying-sfdp.md). 
- Then follow the [ASG-Tool usage instructions](./04-generating-sfdp.md) to generate the SFDP.
