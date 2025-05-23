# ASG-Tool

A Service for creating TEADAL Shared Federated Data Products (SFDPs) automatically using IBM's GIN library that relies on generative AI. 

## Instructions Summary

SFDP generation with ASG-Tool can be performed locally on developer's workstation using documentation provided in this repository:

1. Start with installing the tool according to [ASG installation instructions](./docs/01-installing-asg.md) 
1. Configure the tool: [Configuring the ASG](./docs/02-configuring-asg.md)
1. Preapare the required inputs: [Specifying the SFDP to be created](./docs/03-specifying-sfdp.md)
1. Invoke the tool to generate the data product according to the inputs and the configuration: [Generating the SFDP](./docs/04-generating-sfdp.md)
2. Inspect and validate the generated data product: [Validating the newly created SFDP](./docs/05-validating-sfdp.md)

When the new SFDP is validated and found acceptable for the deployment, proceed to creating TEADAL deployement artifacts and deployment as described [here (TBD)](./docs/06-deploying-sfdp.md).

In addition, it is planned to make the ASG-Tool available on the TEADAL Node. Consult TEADAL Node documentation for the status of this integration and to learn more about enabling and operating the service there (link TBD).

To contribute to the ASG project, follow instructions [here (TBD)](./docs/00-developing-asg.md)

## Examples

The project contains several simple examples:

1. Medical pilot [pre-caching example](./examples/pilot-medical/README.md)
1. Industry pilot [pre-caching example](./examples/pilot-industry/README.md)

### The repo structure

```plaintext
teadal-connectors/
├── README.md                      # This File
├── .gitignore                     # Project gitignore file
├── .reqs/                         # pip of dependencies for running the tool
|                                  # including the GIN wheel
├── config/                        # example configuration files
├── docs/                          # documentation files
├── examples/                      # examples and some older files
├── sfdp-template/                 # all the files required to 
├── transforms/                    # transforms folder 
├── src/                           # Source code files
|   ├── generate_sfdp.py           # Main entry point of the application
```