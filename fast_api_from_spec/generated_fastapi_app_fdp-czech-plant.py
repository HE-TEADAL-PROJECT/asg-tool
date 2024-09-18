from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
import pandas as pd
from transform import handle_transform
from acg.executor import exec
from langchain_core.documents.base import Document
from acg.types import ApiCallInf,ApiCallIssues

app = FastAPI()

# Define FastAPI endpoints
