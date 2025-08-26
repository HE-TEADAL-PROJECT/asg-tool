This output was received while executing on windows workstation with gitbash.

```sh
$ DEBUG=true python src/generate_sfdp.py -fdp_spec examples/openapi-specs/medical-spec.yaml -fdp_url http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01/ -i examples/asg-instructions/Medical-instructions.yaml -o ../2025-08-26-asg-sf
dp-med -c config/ollama-tdl1-granite-20b.yaml
18:16 [DEBUG] utils.setup_logging.30: gin_log_level=INFO
18:16 [DEBUG] utils.setup_logging.31: gin_loggers=['base', 'llm', 'agentic_workflow', 'tool_calling', 'mapping_service']
18:16 [DEBUG] utils.setup_logging.32: noisy_lib_loggers=['httpx', 'openai', '_config', '_base_client', '_trace', '_client']
18:16 [DEBUG] generate_sfdp.<module>.193: creating args parser
18:16 [DEBUG] generate_sfdp.<module>.195: parsing the args
18:16 [DEBUG] generate_sfdp.<module>.197: ready to go args=Namespace(fdp_spec='examples/openapi-specs/medical-spec.yaml', fdp_url='http://medicine01.teadal.ubiwhere.com/fdp-medicine-node01/', fdp_timeout=300, instructions='examples/asg-instructions/Medical-instructions.yaml', api_key='DUMMY_KEY', output='../2025-08-26-asg-sfdp-med', config='config/ollama-tdl1-granite-20b.yaml', transforms='./transforms/')
18:16 [INFO] generate_sfdp.main.164: Starting SFDP generation
18:16 [DEBUG] gin_helper.generate_sfdp.325: enter
18:16 [DEBUG] gin_helper.generate_sfdp.328: loaded fdp_spec
18:16 [DEBUG] gin_helper.generate_sfdp.330: loaded asg_spec
18:16 [DEBUG] openapi_helper.parse_endpoints.79: enter
18:16 [DEBUG] openapi_helper.parse_endpoints.160: returning 2 endpoints
18:16 [DEBUG] openapi_helper.get_sfdp_endpoints.14: enter
18:16 [DEBUG] openapi_helper.get_sfdp_endpoints.70: returning 2 endpoints
18:16 [DEBUG] gin_helper.generate_sfdp.334: will generate 2 endpoints:
[{'method': 'get',
  'path': '/persons',
  'sfdp_endpoint_name': 'persons_endpoint',
  'sfdp_endpoint_path': '/persons_above_30',
  'name': 'GetPersonsAll',
  'parameters': [],
  'description': 'This endpoint returns all the people of age > 30',
  'response_model': {'name': 'Person',
                     'properties': {'person_id': {'type': 'integer'},
                                    'gender_concept_id': {'type': 'integer'},
                                    'year_of_birth': {'type': 'integer'},
                                    'month_of_birth': {'type': 'integer',
                                                       'nullable': True},
                                    'day_of_birth': {'type': 'integer',
                                                     'nullable': True},
                                    'birth_datetime': {'type': 'string',
                                                       'format': 'date-time',
                                                       'nullable': True},
                                    'race_concept_id': {'type': 'integer'},
                                    'ethnicity_concept_id': {'type': 'integer'},
                                    'location_id': {'type': 'integer',
                                                    'nullable': True},
                                    'provider_id': {'type': 'integer',
                                                    'nullable': True},
                                    'care_site_id': {'type': 'integer',
                                                     'nullable': True},
                                    'person_source_value': {'type': 'string',
                                                            'maxLength': 50,
                                                            'nullable': True},
                                    'gender_source_value': {'type': 'string',
                                                            'maxLength': 50,
                                                            'nullable': True},
                                    'gender_source_concept_id': {'type': 'integer',
                                                                 'nullable': True},
                                    'race_source_value': {'type': 'string',
                                                          'maxLength': 50,
                                                          'nullable': True},
                                    'race_source_concept_id': {'type': 'integer',
                                                               'nullable': True},
                                    'ethnicity_source_value': {'type': 'string',
                                                               'maxLength': 50,
                                                               'nullable': True},
                                    'ethnicity_source_concept_id': {'type': 'integer',
                                                                    'nullable': True}}}},
 {'method': 'get',
  'path': '/persons',
  'sfdp_endpoint_name': 'persons_endpoint_2',
  'sfdp_endpoint_path': '/persons_above_60',
  'name': 'GetPersonsAll',
  'parameters': [],
  'description': 'This endpoint returns all the people of age > 60',
  'response_model': {'name': 'Person',
                     'properties': {'person_id': {'type': 'integer'},
                                    'gender_concept_id': {'type': 'integer'},
                                    'year_of_birth': {'type': 'integer'},
                                    'month_of_birth': {'type': 'integer',
                                                       'nullable': True},
                                    'day_of_birth': {'type': 'integer',
                                                     'nullable': True},
                                    'birth_datetime': {'type': 'string',
                                                       'format': 'date-time',
                                                       'nullable': True},
                                    'race_concept_id': {'type': 'integer'},
                                    'ethnicity_concept_id': {'type': 'integer'},
                                    'location_id': {'type': 'integer',
                                                    'nullable': True},
                                    'provider_id': {'type': 'integer',
                                                    'nullable': True},
                                    'care_site_id': {'type': 'integer',
                                                     'nullable': True},
                                    'person_source_value': {'type': 'string',
                                                            'maxLength': 50,
                                                            'nullable': True},
                                    'gender_source_value': {'type': 'string',
                                                            'maxLength': 50,
                                                            'nullable': True},
                                    'gender_source_concept_id': {'type': 'integer',
                                                                 'nullable': True},
                                    'race_source_value': {'type': 'string',
                                                          'maxLength': 50,
                                                          'nullable': True},
                                    'race_source_concept_id': {'type': 'integer',
                                                               'nullable': True},
                                    'ethnicity_source_value': {'type': 'string',
                                                               'maxLength': 50,
                                                               'nullable': True},
                                    'ethnicity_source_concept_id': {'type': 'integer',
                                                                    'nullable': True}}}}]
18:16 [DEBUG] files_helper.load_user_functions.149: enter, folder_path=./transforms/
18:16 [DEBUG] files_helper.load_user_functions.166: module: transform_functions from D:\tdl-proj\asg\asg-tool-test\transforms\transform_functions.py
18:16 [DEBUG] files_helper.load_user_functions.175: function: transform_functions.concatenate_fields
18:16 [DEBUG] files_helper.load_user_functions.175: function: transform_functions.filter_by_quarter
18:16 [DEBUG] files_helper.load_user_functions.175: function: transform_functions.filter_by_year
18:16 [DEBUG] files_helper.load_user_functions.175: function: transform_functions.make_tool
18:16 [DEBUG] files_helper.load_user_functions.175: function: transform_functions.map_field
18:16 [DEBUG] files_helper.load_user_functions.166: module: medical_transform_functions from D:\tdl-proj\asg\asg-tool-test\transforms\med\medical_transform_functions.py
18:16 [DEBUG] files_helper.load_user_functions.175: function: medical_transform_functions.calculate_age
18:16 [DEBUG] files_helper.load_user_functions.175: function: medical_transform_functions.make_tool
18:16 [DEBUG] files_helper.load_user_functions.175: function: medical_transform_functions.persons_above_age
18:16 [DEBUG] gin_helper._get_transforms.27: loaded 8 transform functions
18:16 [DEBUG] gin_helper._get_tr_instructs.169: enter for 2 endpoints
18:16 [DEBUG] gin_helper._get_tr_instructs.173: endpoint name: persons_endpoint
18:16 [DEBUG] gin_helper._get_tr_instructs.182: element name: Person
18:16 [DEBUG] gin_helper._get_tr_instructs.190: property name: person_ID
18:16 [DEBUG] gin_helper._get_prop_tr_instructs.118: enter for persons_endpoint.Person.person_ID
18:16 [DEBUG] gin_helper._get_prop_tr_instructs.123: calling gin with query=map person_id to target: person_ID
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.133: gin has performed 1 iterations
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.136: gin_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.139: gin_static_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.141: gin_llm_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.148: gin has returned with 5 tools context elements
18:19 [DEBUG] gin_helper._get_tr_instructs.190: property name: person_age
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.118: enter for persons_endpoint.Person.person_age
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.123: calling gin with query=the age is above 30 to target: person_age
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.133: gin has performed 1 iterations
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.136: gin_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "input_df", "age": 30, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'input_df', 'age': 30, 'target': 'person_age'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.139: gin_static_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "input_df", "age": 30, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'input_df', 'age': 30, 'target': 'person_age'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.141: gin_llm_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "input_df", "age": 30, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'input_df', 'age': 30, 'target': 'person_age'})]
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.148: gin has returned with 5 tools context elements
18:19 [DEBUG] gin_helper._get_tr_instructs.173: endpoint name: persons_endpoint_2
18:19 [DEBUG] gin_helper._get_tr_instructs.182: element name: Person
18:19 [DEBUG] gin_helper._get_tr_instructs.190: property name: person_ID
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.118: enter for persons_endpoint_2.Person.person_ID
18:19 [DEBUG] gin_helper._get_prop_tr_instructs.123: calling gin with query=map person_id to target: person_ID
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.133: gin has performed 1 iterations
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.136: gin_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.139: gin_static_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.141: gin_llm_api_calls=[ApiCallInf(raw_str='{"name": "map_field", "arguments": {"df": "input_df", "source": "person_id", "target": "person_ID"}}', valid=True, name='map_field', parameters={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.148: gin has returned with 5 tools context elements
18:20 [DEBUG] gin_helper._get_tr_instructs.190: property name: person_age
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.118: enter for persons_endpoint_2.Person.person_age
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.123: calling gin with query=the age is above 60 to target: person_age
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.133: gin has performed 1 iterations
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.136: gin_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "source_df", "age": 60, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'source_df', 'age': 60, 'target': 'person_age'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.139: gin_static_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "source_df", "age": 60, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'source_df', 'age': 60, 'target': 'person_age'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.141: gin_llm_api_calls=[ApiCallInf(raw_str='{"name": "persons_above_age", "arguments": {"df": "source_df", "age": 60, "target": "person_age"}}', valid=True, name='persons_above_age', parameters={'df': 'source_df', 'age': 60, 'target': 'person_age'})]
18:20 [DEBUG] gin_helper._get_prop_tr_instructs.148: gin has returned with 5 tools context elements
18:20 [DEBUG] gin_helper._get_tr_instructs.201: returning 4 elements
18:20 [DEBUG] gin_helper._get_ep_specs.276: enter for 2 endpoints and 4 transforms
18:20 [DEBUG] gin_helper._get_ep_specs.281: ep_name=persons_endpoint, ep_params=[]
18:20 [DEBUG] gin_helper._add_ep_exports.53: enter for persons_endpoint
18:20 [DEBUG] gin_helper._add_ep_exports.59: there are 2 exports for persons_endpoint
18:20 [DEBUG] gin_helper._add_ep_exports.68: processing 1 api calls for persons_endpoint.Person.person_ID
18:20 [DEBUG] gin_helper._add_ep_exports.72: api_call_name=map_field, api_call_params={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'}
18:20 [DEBUG] gin_helper._get_tool_for_call.32: enter for map_field with 5 context elements
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='map_field', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']}, description='map fields or change names from source to target.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.41: found tool for map_field
18:20 [DEBUG] gin_helper._add_ep_exports.78: doc=name='map_field' parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']} description='map fields or change names from source to target.' api_type=<APITypes.FUNCTION: 'function'> call_meta=None(<class 'gin.common.types.ToolDetails'>)
18:20 [DEBUG] gin_helper._add_ep_exports.68: processing 1 api calls for persons_endpoint.Person.person_age
18:20 [DEBUG] gin_helper._add_ep_exports.72: api_call_name=persons_above_age, api_call_params={'df': 'input_df', 'age': 30, 'target': 'person_age'}
18:20 [DEBUG] gin_helper._get_tool_for_call.32: enter for persons_above_age with 5 context elements
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='map_field', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']}, description='map fields or change names from source to target.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='concatenate_fields', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'col1': {'type': 'str', 'description': 'The first column.'}, 'col2': {'type': 'str', 'description': 'The second column.'}, 'output': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'col1', 'col2', 'output']}, description='concatenate Two fields.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='filter_by_year', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'year_col': {'type': 'str', 'description': 'The name of the column containing the year values.'}, 'input_year': {'type': 'integer', 'description': 'The year to filter the DataFrame by.'}, 'required': ['df', 'year_col', 'input_year']}, description='Filters a DataFrame to return rows where the year matches the given input_year.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='filter_by_quarter', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'month_col': {'type': 'str', 'description': 'The name of the column containing the month values.'}, 'quarter': {'type': 'integer', 'description': 'The quarter to filter by (1 for Q1, 2 for Q2, 3 for Q3, 4 for Q4).'}, 'required': ['df', 'month_col', 'quarter']}, description='Filters a DataFrame to return rows where the month falls within the specified quarter.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='persons_above_age', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'age': {'type': 'integer', 'description': 'The age to filter the DataFrame by.'}, 'target': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'age', 'target']}, description='Filters a DataFrame to return rows where the age\n      (calculated from year_of_birth, month_of_birth,day_of_birth) is bigger than the given input_age.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.41: found tool for persons_above_age
18:20 [DEBUG] gin_helper._add_ep_exports.78: doc=name='persons_above_age' parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'age': {'type': 'integer', 'description': 'The age to filter the DataFrame by.'}, 'target': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'age', 'target']} description='Filters a DataFrame to return rows where the age\n      (calculated from year_of_birth, month_of_birth,day_of_birth) is bigger than the given input_age.' api_type=<APITypes.FUNCTION: 'function'> call_meta=None(<class 'gin.common.types.ToolDetails'>)
18:20 [DEBUG] gin_helper._get_ep_specs.281: ep_name=persons_endpoint_2, ep_params=[]
18:20 [DEBUG] gin_helper._add_ep_exports.53: enter for persons_endpoint_2
18:20 [DEBUG] gin_helper._add_ep_exports.59: there are 2 exports for persons_endpoint_2
18:20 [DEBUG] gin_helper._add_ep_exports.68: processing 1 api calls for persons_endpoint_2.Person.person_ID
18:20 [DEBUG] gin_helper._add_ep_exports.72: api_call_name=map_field, api_call_params={'df': 'input_df', 'source': 'person_id', 'target': 'person_ID'}
18:20 [DEBUG] gin_helper._get_tool_for_call.32: enter for map_field with 5 context elements
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='map_field', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']}, description='map fields or change names from source to target.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.41: found tool for map_field
18:20 [DEBUG] gin_helper._add_ep_exports.78: doc=name='map_field' parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']} description='map fields or change names from source to target.' api_type=<APITypes.FUNCTION: 'function'> call_meta=None(<class 'gin.common.types.ToolDetails'>)
18:20 [DEBUG] gin_helper._add_ep_exports.68: processing 1 api calls for persons_endpoint_2.Person.person_age
18:20 [DEBUG] gin_helper._add_ep_exports.72: api_call_name=persons_above_age, api_call_params={'df': 'source_df', 'age': 60, 'target': 'person_age'}
18:20 [DEBUG] gin_helper._get_tool_for_call.32: enter for persons_above_age with 5 context elements
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='map_field', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'source': {'type': 'str', 'description': 'The first column name.'}, 'target': {'type': 'str', 'description': 'The second column name.'}, 'required': ['df', 'source', 'target']}, description='map fields or change names from source to target.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='concatenate_fields', parameters={'df': {'type': 'any', 'description': 'input dataframe.'}, 'col1': {'type': 'str', 'description': 'The first column.'}, 'col2': {'type': 'str', 'description': 'The second column.'}, 'output': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'col1', 'col2', 'output']}, description='concatenate Two fields.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='filter_by_year', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'year_col': {'type': 'str', 'description': 'The name of the column containing the year values.'}, 'input_year': {'type': 'integer', 'description': 'The year to filter the DataFrame by.'}, 'required': ['df', 'year_col', 'input_year']}, description='Filters a DataFrame to return rows where the year matches the given input_year.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='filter_by_quarter', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'month_col': {'type': 'str', 'description': 'The name of the column containing the month values.'}, 'quarter': {'type': 'integer', 'description': 'The quarter to filter by (1 for Q1, 2 for Q2, 3 for Q3, 4 for Q4).'}, 'required': ['df', 'month_col', 'quarter']}, description='Filters a DataFrame to return rows where the month falls within the specified quarter.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.39: tool_details=ToolDetails(name='persons_above_age', parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'age': {'type': 'integer', 'description': 'The age to filter the DataFrame by.'}, 'target': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'age', 'target']}, description='Filters a DataFrame to return rows where the age\n      (calculated from year_of_birth, month_of_birth,day_of_birth) is bigger than the given input_age.', api_type=<APITypes.FUNCTION: 'function'>, call_meta=None)
18:20 [DEBUG] gin_helper._get_tool_for_call.41: found tool for persons_above_age
18:20 [DEBUG] gin_helper._add_ep_exports.78: doc=name='persons_above_age' parameters={'df': {'type': 'any', 'description': 'The input pandas DataFrame.'}, 'age': {'type': 'integer', 'description': 'The age to filter the DataFrame by.'}, 'target': {'type': 'str', 'description': 'the new column name, the target.'}, 'required': ['df', 'age', 'target']} description='Filters a DataFrame to return rows where the age\n      (calculated from year_of_birth, month_of_birth,day_of_birth) is bigger than the given input_age.' api_type=<APITypes.FUNCTION: 'function'> call_meta=None(<class 'gin.common.types.ToolDetails'>)
18:20 [DEBUG] gin_helper._get_ep_specs.312: returning 2 specs
18:20 [DEBUG] gin_helper.generate_sfdp.350: returning {len(endpoints)} endpoints and {len(endpoint_specs)} specs
18:20 [INFO] generate_sfdp.main.180: SFDP generation suceeded, rendering the template
18:20 [INFO] generate_sfdp.main.185: SFDP template rendered, writing output
18:20 [DEBUG] generate_sfdp._write_output.46: copying common files from .\sfdp-template to ../2025-08-26-asg-sfdp-med
18:20 [DEBUG] generate_sfdp._write_output.48: copying .dockerignore
18:20 [DEBUG] generate_sfdp._write_output.48: copying .env
18:20 [DEBUG] generate_sfdp._write_output.48: copying .gitattributes
18:20 [DEBUG] generate_sfdp._write_output.48: copying .gitignore
18:20 [DEBUG] generate_sfdp._write_output.48: copying .gitlab-ci.yml
18:20 [DEBUG] generate_sfdp._write_output.48: copying Dockerfile
18:20 [DEBUG] generate_sfdp._write_output.48: copying Dockerfile_from_src
18:20 [DEBUG] generate_sfdp._write_output.48: copying Dockerfile_from_img
18:20 [DEBUG] generate_sfdp._write_output.48: copying pyproject.toml
18:20 [DEBUG] generate_sfdp._write_output.48: copying README.md
18:20 [DEBUG] generate_sfdp._write_output.48: copying requirements-base.txt
18:20 [DEBUG] generate_sfdp._write_output.48: copying requirements-dev.txt
18:20 [DEBUG] generate_sfdp._write_output.48: copying requirements-local.txt
18:20 [DEBUG] generate_sfdp._write_output.51: copying transform files from ./transforms/ to ../2025-08-26-asg-sfdp-med\transforms
18:20 [DEBUG] files_helper.process_file.86: processed: D:\tdl-proj\asg\asg-tool-test\transforms\transform_functions.py -> D:\tdl-proj\asg\2025-08-26-asg-sfdp-med\transforms\transform_functions.py
18:20 [DEBUG] files_helper.process_file.86: processed: D:\tdl-proj\asg\asg-tool-test\transforms\med\medical_transform_functions.py -> D:\tdl-proj\asg\2025-08-26-asg-sfdp-med\transforms\med\medical_transform_functions.py
18:20 [DEBUG] generate_sfdp._write_output.63: writing contents to ../2025-08-26-asg-sfdp-med\app.py
18:20 [INFO] generate_sfdp.main.188: SFDP app generation complete, the code is in ../2025-08-26-asg-sfdp-med\app.py
```