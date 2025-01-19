# TEADAL-GIN-ASG
  Create Shared Federated data product automatically using IBM's GIN solution.
## project structure
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


## How to Run

1. **Clone the repository**:
   ```bash
   git clone git@github.ibm.com:mc-connectors/teadal-connectors.git
   cd teadal-connectors
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

Requires access to the corporate IBM github to pull GIN library.
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

To generate the SFDP server application, you need to provide the following command line parameters:
- The OpenAPI specification of the source FDP as `-spec` parameter
- The URL of the source FDP as `-fdp_server` parameter
- The ASG instructions file describing the SFDP to be generated as `-i` parameter
- The ASG congiguration file required for accessing and configuring the OpenAI service, as `-c` parameter

   ```bash
   python src/generate_sfdp.py -spec <PATH_TO_FDP_OPENAPI_SPEC> -i <SFDP_GENERATION_INSTRUCTION_FILE> -fdp_server <FDP_URL> -c <GIN_TEADAL_CONFIG_FILE>
   ```


## Running the generated SFDP server

 - Run the server using the command - 
  ```bash
  uvicorn generated_servers.{{generated_fastapi_app_name}}:app --reload # where {{generated_fastapi_app}} is one of the generated FastAPI apps.
  ```
 - The server will run on localhost port 8000.
 - From the browser or any rest client, send a request to the running server on localhost:
     for example: stops: http://localhost:8000/stops/
     the response will be returned as json.


## ASG Specification file structure 

This section describes the structure of the YAML file used for defining the mappings between SFDP and FDP endpoints, including schema definitions for the associated data.

### Top-Level Structure

- **`sfdp_endpoints`**: A list of endpoint mappings. Each item in this list represents a specific endpoint and its associated configurations.

### Endpoint Mapping Structure

Each endpoint mapping under `sfdp_endpoints` is a dictionary with the following keys:

  - **`<endpoint_name>`**: The name of the endpoint (e.g., `stops_endpoint`).
  - **`fdp_path`**: (String) The path to the FDP endpoint. It is a string with placeholders for dynamic segments (e.g., `/stops/stop_id/{stop_id}`).
  - **`sfdp_path`**: (String) The path to the SFDP endpoint. It mirrors the FDP path with similar placeholders (e.g., `/stop_id/{stop_id}`).
  - **`schema`**: A dictionary defining the schema for the data associated with the endpoint. This section describes the data types and structures expected for the response or request payloads.

### Schema Structure

The `schema` key contains one or more schema definitions. Each schema is a dictionary with the following keys:

- **`<schema_name>`**: The name of the schema (e.g., `Stop`). It defines the structure of the data model.
  - **`type`**: (String) The type of the schema. It is usually `object` to indicate a structured object.
  - **`properties`**: A dictionary that defines the properties of the schema object. Each property has its own definition.

#### Property Definition

Each property in the `properties` dictionary has the following keys:

- **`<property_name>`**: The name of the property (e.g.,`stop_full_name`). It identifies a specific field within the schema.
  - **`type`**: (String) The data type of the property (e.g., `integer`, `string`). It defines the type of data this property holds.
  - **`example`**: (Optional) An example value for the property. It illustrates a sample data value that conforms to the property's type.
  - **`description`**: (String) A brief description of the property. It explains what the property represents and how is it constructred from the FDP endpoint's (fdp_path) ouput data model.

## Example Structure

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

## Creating an image to run the SFDP server in a conatiner
TODO