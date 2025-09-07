import json
from typing import Any
from gin.common.types import ToolDetails, ApiCallInf
from gin.common.con_spec import (
    ConnectorSpec,
    Metadata,
    Server,
    TransformFunction,
    ProcessDataSet,
    Output,
    Dataset,
    Call,
    ApiCall,
    Argument,
    CallTypeEnum,
    MethodEnum,
    ArgLocationEnum,
    ArgSourceEnum,
)
from gin.gen.agents.tool_calling import simple_tool_calling as gin_tool_calling
from gin.common.tool_decorator import tool_metadata_list as gin_tool_metadata

from models.sfdp_spec import SFDPEndpoint
from models.asg_spec import ASGResponseSchema
from models.openapi_spec import OpenApiParameter
from utils.files_helper import load_functions as load_user_functions
from utils.log_helper import logger


class GinHelper:
    gin_config_path: str
    transforms_path: str
    transform_functions: list[ToolDetails]

    def __init__(self, gin_config_path: str, transforms_path: str):
        self.gin_config_path = gin_config_path
        self.transforms_path = transforms_path
        self.transform_functions = self._load_transforms()

    def _load_transforms(self) -> list[ToolDetails]:
        """
        Loads functions from python modules found in the provided folder
        Loading affects GIN's gin_tool_metadata object
        """
        loaded_functions = load_user_functions(folder_path=self.transforms_path)
        logger.debug(f"loaded {len(loaded_functions)} transform functions")
        result = [transform.model_dump() for transform in gin_tool_metadata]
        return result

    def _gin_generate_transforms(self, gin_query: str) -> list[TransformFunction]:
        """
        Wraps our call to gin_tool_calling method which returns custon dictionary:
        - conf: BaseConfig          - the utilized config
        - user_input: str           - the original query
        - issues: str               ?
        - missing_value_int: str    ?
        - context: list[Document]   + we need metadata["tool_details_str"]
        - api_calls: list[ApiCallInf]     + we need
                    ApiCallInf(
                        raw_str='{"name": "persons_above_age", "arguments": {"df": "source_df", "age": 60, "target": "person_age"}}',
                        valid=True,
                        name='persons_above_age',
                        parameters={'df': 'source_df', 'age': 60, 'target': 'person_age'}
                    )
            )
        - static_api_calls: list[ApiCallInf]  ?
        - LLM_api_calls: : list[ApiCallInf]   ?
        - 'iter_count': int           + how many times llm was called
        - 'feedback':                 ?
        - 'static_issues': list[ApiCallStaticIssues]  ?
        """
        # returns
        gin_result = gin_tool_calling(
            functions=self.transform_functions,
            query=gin_query,
            config_file=self.gin_config_path,
        )

        if not gin_result:
            logger.warning("gin did not return any result :-(")
            return []

        gin_iter_count = gin_result.get("iter_count")
        logger.debug(f"gin has performed {gin_iter_count} iterations")

        gin_api_calls: ApiCallInf = gin_result.get("api_calls")
        logger.debug(f"gin returned api_calls: {gin_api_calls}")

        gin_static_api_calls: ApiCallInf = gin_result.get("static_api_calls")
        logger.debug(f"gin returned static_api_calls: {gin_static_api_calls}")

        gin_llm_api_calls: ApiCallInf = gin_result.get("LLM_api_calls")
        logger.debug(f"gin returned llm_api_calls: llm_api_calls{gin_llm_api_calls}")

        gin_context = gin_result.get("context")
        prop_context_tools: list[ToolDetails] = get_context_tools(gin_context)
        logger.debug(f"gin returned {len(prop_context_tools)} context tools")

        prop_transforms = _transform_functions(list(gin_api_calls), prop_context_tools)
        logger.debug(f"prop_transforms: {prop_transforms}")

        return prop_transforms

    def _transform_with_params(
        self,
        prop_data: dict,
        transform: TransformFunction,
    ) -> TransformFunction:
        reverse_map = {}

        for param in prop_data.get("linked_params", []):
            reverse_map[param.example] = param.ref
        new_params = {}
        for key, value in transform.params.items():
            if value in reverse_map:
                new_params[key] = reverse_map[value]
            else:
                new_params[key] = value

        return TransformFunction(
            function=transform.function,
            description=transform.description,
            params=new_params,
            output=transform.output,
        )

    def generate_endpoint_spec(self, sfdp_ep: SFDPEndpoint) -> ConnectorSpec | None:

        ep_name: str = sfdp_ep.sfdp_ep_name
        ep_responses: list[ASGResponseSchema] = sfdp_ep.sfdp_ep_responses
        ep_exports = {}
        logger.debug(f"\n\nhandling endpoint: name={ep_name}, schema={ep_responses}")

        for ep_response in ep_responses:
            resp_name = ep_response.name
            resp_props = ep_response.properties
            logger.debug(f"resp_name={resp_name}, resp_props={resp_props})")
            if not resp_props:
                logger.warning(
                    f"no properties defined for {ep_name}.{resp_name}, skipping"
                )
                continue

            resp_fields: dict[str, list[TransformFunction]] = {}
            for prop_name, prop_data in resp_props.items():
                prop_transforms = []
                if not prop_data:
                    logger.debug(
                        f"no transform is needed for {ep_name}.{resp_name}.{prop_name}"
                    )
                else:
                    gin_query = f"{prop_data.get('resolved_description')} to target: {prop_name}"
                    logger.debug(
                        f"calling gin to generate transforms for {ep_name}.{resp_name}.{prop_name}: prop_data={prop_data}, gin_query={gin_query}"
                    )
                    transforms_with_values = self._gin_generate_transforms(gin_query)
                    logger.debug(f"gin generated transforms: {transforms_with_values}")
                    for transform in transforms_with_values:
                        transform_with_params = self._transform_with_params(
                            prop_data=prop_data, transform=transform
                        )
                        prop_transforms.append(transform_with_params)
                # here we set the generated transforms list or []
                resp_fields[prop_name] = prop_transforms
            logger.debug(f"resp_fields={resp_fields}({type(resp_fields)})")
            resp_dataset = ProcessDataSet(
                # TODO figure why this is hardcoded as .
                dataframe=".",
                fields=resp_fields,
            )
            logger.debug(f"ep_process_dataset={resp_dataset}")

        ep_exports[resp_name] = resp_dataset
        logger.debug(f"ep_exports={ep_exports}")

        return create_gin_con_spec(sfdp_ep=sfdp_ep, ep_exports=ep_exports)


# here come miscelanious methods for manipulating GIN spec objects
def get_context_tools(gin_context: list | None) -> list[ToolDetails]:
    """
    gin returns context as
        context: list[langchain_core.documents.base.Document]
    each document has:
        - page_content: str
        - metadata: dict[str,str] with one element: tool_details_str
        metadata: dict
    from each metadata dictionalry we need to extract
        tool_details_str: str ["tool_details_str] that can be transformed to a ToolDetails object
    """
    result: list[ToolDetails] = []

    if not gin_context:
        return result

    for context_entry in gin_context:
        # logger.debug(f"\n\ncontext_entry={context_entry}({type(context_entry)})")
        context_md_dict = context_entry.metadata

        tool_details_str = context_md_dict.get("tool_details_str")
        tool_details_dict = json.loads(tool_details_str)
        tool_details = ToolDetails(**tool_details_dict)
        result.append(tool_details)

    return result


def _transform_functions(
    api_calls: list[ApiCallInf], tools: list[ToolDetails]
) -> list[TransformFunction]:
    """
    ToolDetails (from gin tool calling)
        - name: str
        - parameters: dict
        - description: str
        - api_type: APITypes    ?
        - call_meta             ?
    TransformFunction   (in endpoint spec)
        - function: str
        - description: str = ""
        - params: dict[str, Any] | None = None
        - output: str = ""
    """
    result: list[TransformFunction] = []

    for api_call in api_calls:
        if not api_call.valid:
            logger.warning(f"api_call={api_call} is not valid")

        api_name = api_call.name
        logger.debug(f"api call name: {api_name}")

        api_params: dict[str, Any] = api_call.parameters
        logger.debug(f"api call params: {api_params}")

        # get rid of 'df' TODO figure why this is needed
        if "df" in api_params:
            del api_params["df"]

        for tool in tools:
            if tool.name == api_name:
                transform_function = TransformFunction(
                    function=api_name,
                    description=tool.description,
                    params=api_params,
                )
                logger.debug(f"adding transform_function: {transform_function}")
                result.append(transform_function)

    return result


def create_gin_con_spec(
    sfdp_ep: SFDPEndpoint, ep_exports: dict[str, ProcessDataSet]
) -> ConnectorSpec:
    ep_name = sfdp_ep.sfdp_ep_name
    logger.debug(f"creating connector spec for {ep_name}")

    metadata = Metadata(
        name=f"{ep_name}",
        description=f"SFDP connector to {sfdp_ep.fdp_ep_name}",
        inputPrompt=f"{sfdp_ep.sfdp_ep_descr}",
    )
    logger.debug(f"metadata: {metadata}")

    servers = [Server(url=sfdp_ep.url)]
    logger.debug(f"servers: {servers}")

    spec: Call = create_gin_call(sfdp_ep, ep_exports)
    logger.debug(f"spec: {spec}")
    # p_params_dict =  sfdp_ep.fdp_ep_p_params
    # q_params_dict =  sfdp_ep.fdp_ep_p_params

    # api_calls = spec.apiCalls
    # logger.debug(f"api_calls: {api_calls}")

    # for api_call_name, api_call_details in api_calls.items():
    #     logger.debug(f"api_call {api_call_name}: api_call_details")
    #     api_call_args = api_call_details.arguments
    #     logger.debug(f"api_call_args: {api_call_args}")
    #     for arg in api_call_args:
    #         arg_name = arg.name
    #         logger.debug(f"arg {arg_name}: {arg}")
    #         if arg.argLocation == 'parameter':
    #             new_arg_value = p_params_dict.get(arg_name)
    #         if arg.argLocation == 'query':
    #             new_arg_value = q_params_dict.get(arg_name)
    #         if not new_arg_value:
    #             logger.warnig(f"api_call_args: {api_call_args}")
    #             continue
    #         arg.value = new_arg_value

    return ConnectorSpec(metadata=metadata, spec=spec, servers=servers)


# class Call(BaseModel):
#     apicalls: Dict[str, ApiCall] = Field(alias="apiCalls")
#     output: Output
#     timeout: Optional[int] = 60
def create_gin_call(
    sfdp_ep: SFDPEndpoint, ep_exports: dict[str, ProcessDataSet]
) -> Call:

    output_name = sfdp_ep.fdp_ep_response
    logger.debug(f"call output_name: {output_name}")

    output_dataset = Dataset(
        api=sfdp_ep.fdp_ep_name,
        metadata=[],
        path=".",
    )
    logger.debug(f"call output_dataset: {output_dataset}")

    call_output = Output(
        data={output_name: output_dataset},
        exports=ep_exports,
        execution="",
        runtime_type="python",
    )
    logger.debug(f"call_output: {call_output}")

    apicall = create_gin_api_call(sfdp_ep)
    logger.debug(f"apicall: {apicall}")

    apicalls = {sfdp_ep.fdp_ep_name: apicall}
    logger.debug(f"apicalls: {apicalls}")

    return Call(
        apiCalls=apicalls,  # Dict[str, ApiCall]
        output=call_output,  # Output
        timeout=sfdp_ep.timeout,  # Optional[int] = 60
    )


def create_gin_api_call(
    spdp_ep: SFDPEndpoint,
) -> ApiCall:
    """
    This is how gin object looks like:

    class ApiCall(BaseModel):
        type: CallTypeEnum
        endpoint: str
        method: MethodEnum
        arguments: Optional[List[Argument]] = None
        pagination: Optional[Pagination] = None
    """
    fdp_ep_path = spdp_ep.fdp_ep_path

    api_call = ApiCall(
        type=CallTypeEnum.URL,
        endpoint=fdp_ep_path,
        method=MethodEnum.GET,
    )

    fdp_ep_params = spdp_ep.fdp_ep_params
    if fdp_ep_params and len(fdp_ep_params):
        logger.debug(
            f"creating call args for fdp_ep_path={fdp_ep_path}, fdp_ep_params={fdp_ep_params}"
        )

        arguments: list[Argument] = create_gin_arguments(fdp_ep_params)
        logger.debug(f"arguments={arguments} ")
        api_call.arguments = arguments

    return api_call


def create_gin_arguments(
    fdp_ep_params: list[OpenApiParameter],
) -> list[Argument]:
    """
    This is how gin object looks like:

    class Argument(BaseModel):
        name: str
        argLocation: ArgLocationEnum
        type: ArgTypeEnum
        source: ArgSourceEnum
        value: Any
    """
    result: list[Argument] = []

    for fdp_ep_param in fdp_ep_params:
        arg_name = fdp_ep_param.name
        if fdp_ep_param.schema_ and fdp_ep_param.schema_.type:
            arg_type = fdp_ep_param.schema_.type
        if fdp_ep_param.in_ == "path":
            # path parameter
            arg_value = f"path_params[{arg_name}]"
        elif fdp_ep_param.in_ == "query":
            # query param
            arg_value = f"query_params[{arg_name}]"

        logger.debug(f"arg_name={arg_name}, type = {arg_type}, arg_value={arg_value}")
        arg = Argument(
            name=arg_name,
            argLocation=ArgLocationEnum.PARAMETER,
            type=arg_type or "",
            source=ArgSourceEnum.CONSTANT,
            value=arg_value,
        )
        logger.debug("arg={arg} ")
        result.append(arg)

    logger.debug("result={result} ")
    return result
