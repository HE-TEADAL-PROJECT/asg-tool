# Industry Pilot Example

Examples are created to be run for the Industry Pilot FDP deployed at `http://88.157.206.142/fdp-industry-czech/`, that exposes the OpenAPI [specification](./inputs/fdp-ind-czech-plant.yaml). For other FDPs, please change the corresponding input parameters, the the `fdp_url` and `fdp_spec`

ASG instruction examples are located in the [input folder](./inputs/). 

## Generating the SFDP

To generate SFDP, you need to be in the virtual environment created for the base ASG project, select your input values, and execute, for example, the following command

```sh
# cd to the ASG project root and activate its virtual environment 
# (create this virtual environment if it does not yet exist)

# note the rather long timeout is required here

DEBUG=true python src/generate_sfdp.py \
-fdp_spec examples/pilot-industry/inputs/fdp-ind-czech-plant.yaml  \
-fdp_url http://88.157.206.142/fdp-industry-czech/ \
-fdp_timeout 3333 \ 
-i examples/pilot-industry/inputs/czech-plant-sales-map.yaml   \
-c config/ollama-tdl1-granite-20b.yaml \
-o examples/pilot-industry/result
```

The first time the command is executed for the specified output directory (`-o` parameter), the output directory will be created if it does not exist and will be populated with files required to initialize the new SFDP project, such as `requirements.txt` and `app.py`. 

If the command is executed several times for the same output directory (`-o` parameter), 
only the new FastApi `app<n>.py` file will be added, where `n` is the next consequitive number. 

## Invoking the SFDP

To invoke the SFDP, you need to be in the output directory (specified as the `-o` parameter to the command above), create a new virtual environment there:

```sh
# cd to the output folder specified to the generation command
# create and activate virtual environment

pip install -r requirements.txt

DEBUG=true fastapi dev [appN.py]
```