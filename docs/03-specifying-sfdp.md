# Specifying the SFDP to be generated

ASG tool creates the SFDP as a FASTAPI application that serves data obtained from a source FDP, specified as `-fdp_url <url>` and `fdp_spec <path-to-file>` input paramaters, and transformed as decribed in a separate specification file that ASG tool receives as `-i <path-to-file>` (`i` here stands for the `instructions` :-) input parameter.

## ASG Specification Format 

ASG specification file for SFDP creation contains only one top-level entry, `sfdp_endpoints`, that lists all the endpoints that will be available in the generated FastAPI application. Each item in this list represents a specific endpoint analong with info about how it is derived from the data obtained from the source FDP. 

The general structure of the specification file is as follows:
```yaml
sfdp_endpoints: 
    # the fist endpoint to be generated
    - <endpoint1-name>:
        fdp_path: < path to the endpoint in the source FDP >
        sfpd_path: < path to the endpoint in the generated SFDP >
        sfdp_endpoint_description: < String describing the generated SFDP endpoint >

        schema:
            # what will be returned by the generated endpoint
            <schema-name>:
                type: < object | ? >
                properties:
                    # the first 'column' in the return data
                    <property1-name>:
                        type: < string | integer | number | ? >
                        example: < example value >
                        description: < string describing the property >

                    # more properties can follow

    # more enpoints can follow
```

### Specifying SFDP Endpoints
Each entry under **`sfdp_endpoints`** represents one endpoint to be included in the generated SFDP, named as the entry itself. Each such entry is a dictionary with the following elements:
- **`fdp_path`**: This key is required and must contain a string representing the path to the corresponding endpoint existing in the source FDP. The string can contain placeholders for dynamic segments (e.g., `/stops/stop_id/{stop_id}`).
- **`sfdp_path`**: This key is required and must contain a string representing the path to the generated SFDP endpoint. It can mirror the placeholders in the source FDP path with similar placeholders (e.g., `/stop_id/{stop_id}`).
- **`sfdp_endpoint_description`**: This element is optional and can contain a string with the description of the generated SFDP endpoint. This is not required by the ASG tool and is used only as part of the OpenAPI specification of the generated SFDP, to help SFDP users by explaining the endpoints available from the generated SFDP. 
- **`schema`**: This element is required and must contain a dictionary defining the schema for the data to be returned by the endpoint. This disctionary describes the data properties along with their types and structures, along with the well-formed descriptions that will help ASG tool to derive the required data items from data exposed by the corresponding endpoint of the source FDP. 

### Specifying Data Schemas for the SFDP endpoints
>? can there really be more than one schemas as stated in the [old readme](../README.md)

The **`schema`** structure is a dictionary named as the data structure it describes, with the following keys:
- **`type`**: (String) The type of the data described by the schema. It is usually `object` to indicate a structured dat object.
- **`properties`**: A dictionary that defines the properties of the data described by the schema with `type: object`. Each property must contain name, type, and description, formatted as specified next.

### Specifying individual data elements as part of SFDP Data Schemas
>? maybe we can include both the regular description, to become part of the OpenAPI spec of the generated SFDP, and another, more structured description that helps constructing the required property from the source data.

Each data element returned by the generated SFDP enpoint is specified as an entry in the **`properties`** dictionary. The entries are named as the data elements they specify and contain the following keys:
- **`type`**: This key is required and must contain a string defining the data type for the property (e.g., `integer`, `string`). 
- **`example`**: This key is optional and can contain an example value for the property. This is not required by the ASG tool and is used only as part of the OpenAPI specification of the generated SFDP, to help SFDP users by illustrating a sample data value that conforms to the property's type.
- **`description`**: This key is required and must contain a string describing this property. This is used by the ASG tool to derive the way this property can be constructed from the data exposed by the source FDP endpoint. 

## Examples


