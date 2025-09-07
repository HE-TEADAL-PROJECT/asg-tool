import pytest
from utils.files_helper import load_functions
from gin.common.tool_decorator import tool_metadata_list as gin_tool_metadata
import logging
logger = logging.getLogger("test_gin_helper")

def test_load_transforms():
    logger.debug(f"gin_tool_metadata before loading transforms: {gin_tool_metadata}")
    loaded_functions = load_functions(folder_path="./transforms")
    logger.debug(f"loaded_functions={loaded_functions}")
    logger.debug(f"after gin_load_functions gin_tool_metadata={gin_tool_metadata}")
    functions = [transform.model_dump() for transform in gin_tool_metadata]
    logger.debug(f"functions={functions}")