# Validating the generated SFDP

After sucessful SFDP generation as described [here](./generating-sfdp.md), changed to the output folder (as spesified by the `-o` parameter)

The folder should contail the SFDP server code in `app.py`, the `requirements.txt` file, the `wheel` for the `GIN executor` dependency and the directory with all the transformation code to be executed by the server.

To validate the generated SFDP:
- Create and activate virtual environment with `python3.12`
```sh
$ which python
$ python --version
$ python -m venv .venv
$ . .venv/Scripts/activate  # on Windows
$ . .venv/bin/activate      # On Linux
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

- Examine the server functionality, e.g. using `curl` or browser. Note that `/docs` path should present the swagger UI and the `/openapi.json` path provides the openapi spec for the generated SFDP that can be saved and used for provisioning in the catalog.