# TEADAL-GIN-ASG
  Create Shared Federated data product automatically using IBM's GIN solution.
## project structure
```plaintext
teadal-connectors/
├── src/                           # Source code files
│   ├── generate_sfdp.py           # Main entry point of the application
│
├── asg-instructions/              # Example (input) folder contating ASG specification file for SFDP Generation
│   ├── Medical-instructions.yaml  # Example SFDP generation instructions file
│
├── config/                        # Configuration files
│   └── gin-teadal-config.yaml     # default configuration file
│
├── openapi-specs/                 # openAPI specification for FDP servers
│   └── medical-spec.yaml          # example openAPI specification in yaml format
│
├── transform/                     # Custom User's transfrom functions library 
│   └── transform_function.py      # Each tool must be decorate with @make_tool and has full docstring
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
   cd teadal-connecotrs
   ```

2. **Set up the virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
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


## Creating an image to run the SFDP server in a conatiner
TODO