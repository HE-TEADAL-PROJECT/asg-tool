# TEADAL-GIN-ASG

Create TEADAL Shared Federated Data Products (SFDPs) automatically using IBM's GIN solution. 

## Instructions Summary (TLDR :-)

SFDP generation with ASG can be performed locally on developer's workstation. For this, start with [ASG installation instructions](./docs/01-installing-asg.md) and proceed to the next steps: [Configuring the ASG](./docs/02-configuring-asg.md), [Specifying the SFDP to be created](./docs/03-specifying-sfdp.md), [Generating the SFDP](./docs/04-generating-sfdp.md), and, finally, [Validating the newly created SFDP](./docs/05-validating-sfdp.md).

When the new SFDP is validated and found acceptable for the deployment, proceed to creating TEADAL deployement artifacts and deployment as described [here (TBD)](./docs/06-deploying-sfdp.md).

In addition, ASG service is available on the TEADAL Node. Consult TEADAL Node documentation for enabling and operating the service there (link TBD).

To contribute to the ASG project, follow instructions [here (TBD)](./docs/00-developing-asg.md)

## Examples

The project contains several simple examples:

1. Medical pilot [example](./examples/pilot-medical/README.md)

### More Details

> !!! some of the information below might be outdated <br>
> !!! please follow links in the summary above <br>

### ASG project structure

```plaintext
teadal-connectors/
├── src/                           # Source code files
│   ├── generate_sfdp.py           # Main entry point of the application
│
├── asg-instructions/              # Example (input) folder containing ASG specification file for SFDP Generation
│   ├── Medical-instructions.yaml  # Example SFDP generation instructions file
│
├── config/                        # Configuration files
│   └── gin-teadal-config.yaml     # default configuration file
│
├── openapi-specs/                 # openAPI specification for FDP servers
│   └── medical-spec.yaml          # example openAPI specification in yaml format
│
├── transform/                     # Custom transform functions library 
│   └── transform_function.py      # Each tool must be decorated with @make_tool and have a full docstring
│
├── generated_servers/             # Output folder - FastAPI applications
│   └── sfdp-server1.py            # FastAPI application code generated automatically
│
├── examples/                      # Some usage notebook examples (for pocs)
│   └── conn_gen_example.ipynb     # Example notebook
│
├── Dockerfile                     # Dockerfile example to create an image running the SFDP server
├── README.md                      # Project documentation
│
│
├── .gitignore                     # Project gitignore file
│
└── requirements.txt               # List of dependencies
```

### ASG Specification file structure 

This section describes the structure of the YAML file used for defining the mappings between SFDP and FDP endpoints, including schema definitions for the associated data.

#### Top-Level Structure

- **`sfdp_endpoints`**: A list of endpoint mappings. Each item in this list represents a specific endpoint and its associated configurations.

#### Endpoint Mapping Structure

Each endpoint mapping under `sfdp_endpoints` is a dictionary with the following keys:

  - **`<endpoint_name>`**: The name of the endpoint (e.g., `stops_endpoint`).
  - **`fdp_path`**: (String) The path to the FDP endpoint. It is a string with placeholders for dynamic segments (e.g., `/stops/stop_id/{stop_id}`).
  - **`sfdp_path`**: (String) The path to the SFDP endpoint. It mirrors the FDP path with similar placeholders (e.g., `/stop_id/{stop_id}`).
  - **`sfdp_endpoint_description`**: (String) The description of the SFDP endpoint.
  - **`schema`**: A dictionary defining the schema for the data associated with the endpoint. This section describes the data types and structures expected for the response or request payloads.

#### Schema Structure

The `schema` key contains one or more schema definitions. Each schema is a dictionary with the following keys:

- **`<schema_name>`**: The name of the schema (e.g., `Stop`). It defines the structure of the data model.
  - **`type`**: (String) The type of the schema. It is usually `object` to indicate a structured object.
  - **`properties`**: A dictionary that defines the properties of the schema object. Each property has its own definition.

##### Property Definition

Each property in the `properties` dictionary has the following keys:

- **`<property_name>`**: The name of the property (e.g.,`stop_full_name`). It identifies a specific field within the schema.
  - **`type`**: (String) The data type of the property (e.g., `integer`, `string`). It defines the type of data this property holds.
  - **`example`**: (Optional) An example value for the property. It illustrates a sample data value that conforms to the property's type.
  - **`description`**: (String) A brief description of the property. It explains what the property represents and how is it constructred from the FDP endpoint's (fdp_path) ouput data model.

#### Example Structure

```yaml
sfdp_endpoints:
  - <endpoint_name>:
      fdp_path: <fdp_path_string>
      sfdp_path: <sfdp_path_string>
      schema:
        <schema_name>:
          type: object
          properties:
            <property_name>:
              type: <property_type>
              example: <example_value>
              description: <property_description>
```

### Creating an image to run the SFDP server in a conatiner
After creating the SFDP server, Dockerfile has the needed commands and copies the needed files to be able to run the server in a container (e.g copying the server, copying the user defined functions, installing the requirements to run the executor).

From root folder, run the following:
 ### building the image
   Windows:
   ```bash
    DOCKER_BUILDKIT=1 docker build  --ssh default=<id_rsa_path>   --progress=plain   -t my-sfdp-app .
   ```
   Mac/Linux:
   ```bash
    docker build -ssh default -t my sfdp-app
   ```
 ### Running the image as a container
  ```bash
  docker run -p 8000:8000 my-sfdp-app
  ```
