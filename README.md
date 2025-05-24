# ASG-Tool

A Service for creating TEADAL Shared Federated Data Products (SFDPs) automatically using IBM's GIN library that relies on generative AI. 

## Instructions Summary

SFDP generation with ASG-Tool can be performed locally on developer's workstation using documentation provided in this repository:

1. Start with installing the tool according to [ASG installation instructions](./docs/01-installing-asg.md) 
1. Configure the tool as described in [Configuring the ASG](./docs/02-configuring-asg.md)
1. Prepare the inputs required for generating data product according to  a data sharing agreement, as described in [Specifying the SFDP to be created](./docs/03-specifying-sfdp.md)
1. Invoke the tool to generate the data product according to the inputs and the configuration, as described in [Generating the SFDP](./docs/04-generating-sfdp.md)
2. Inspect and validate the generated data product, e.g., as shown in [Validating the newly created SFDP](./docs/05-validating-sfdp.md)

When the new SFDP is validated and found acceptable for the deployment, proceed to creating TEADAL deployement artifacts and to promoting the SFDP to deployment as described [here (TBD)](./docs/06-deploying-sfdp.md).

It is planned to make the ASG-Tool available on the TEADAL Node. Consult TEADAL Node documentation for the status of this integration and to learn more about enabling and operating the service there (link TBD).

To contribute to the ASG project, follow instructions [here (TBD)](./docs/00-developing-asg.md)

## Examples

The project contains several simple examples.

These two examples are powered by the GIN Executor. They are fully functional data product but do not have additional capabilities, such as caching, encoding, etc.
1. Medical Pilot [pre-caching example](./examples/pilot-medical/README.md)
1. Industry Pilot [pre-caching example](./examples/pilot-industry/README.md)

These new examples are powered by the ASG-Runtime and, in addition to serving the defined data endpoints, include service endpoints and can be configured to cache and encode the data.
1. Medical pilot [example with caching (TBD)](./examples/sfdp-med/README.md)
1. Industry pilot [example with caching](./examples/sfdp-ind/README.md)
1. Viticulture pilot [example with caching (TBD)](./examples/sfdp-vit-new/README.md)
1. Mobility pilot [example with caching (TBD)](./examples/pilot-mob-new/README.md)
1. Financial pilot [example with caching (TBD)](./examples/pilot-fin-new/README.md)
1. Regional Planning pilot [example with caching (TBD)](./examples/pilot-reg-new/README.md)

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

