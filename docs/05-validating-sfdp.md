# Validating the generated SFDP

After sucessful SFDP generation as described [here](./04-generating-sfdp.md), `cd` to the output folder (the one that was spesified by the `-o` parameter).

The folder should contain the SFDP server code in `app.py`, the `requirements.txt` file, the `wheel` for the `GIN executor` dependency (TBD change when this is replaced by gitlab ref) and the directory with the transformation code to be executed by the server.

To validate the generated SFDP:
- Create and activate virtual environment with `python3.12`
```sh
$ which python
$ python --version
$ python -m venv .venv

# on Windows
$ . .venv/Scripts/activate  
# On Linux
$ . .venv/bin/activate     
```

- upgrade pip and install the dependencies
```sh
$ python -m pip install --upgrade pip
$ python -m pip install -r requirements.txt
```

- Run the server
```sh
uvicorn app:app --reload

# to enable debug messages from the executor, run
DEBUG=true uvicorn app:app
```

You can now examine the server functionality, e.g. with `curl` or with the browser, probing for all the endpoints that SFDP must support. 

For your convenience, you can see the following additional endpoints:
- `/info` path presents the settings the generated service is running with, e.g. the `DEBUG` setting

- `/docs` path presents the swagger UI for convenient probing using the same browser window.

- `/openapi.json` path provides the openapi spec for the generated SFDP that can be saved and used for provisioning in the catalog.