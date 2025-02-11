# Validating the generated SFDP

After sucessful SFDP generation as described [here](./generating-sfdp.md), `cd` to the output folder (the one that was spesified by the `-o` parameter).

The folder should contain the SFDP server code in `app.py`, the `requirements.txt` file, the `wheel` for the `GIN executor` dependency and the directory with the transformation code to be executed by the server.

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
```

You can now examine the server functionality, e.g. with `curl` or with the browser, probing for all the endpoints that SFDP must support. 

Note that `/docs` path should present the swagger UI for convenient probing using the same browser window.

Also nothe that the `/openapi.json` path provides the openapi spec for the generated SFDP that can be saved and used for provisioning in the catalog.