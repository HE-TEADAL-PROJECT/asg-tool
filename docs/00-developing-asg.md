# Developing the ASG

If you are making changes to asg_tool repo, validate your changes work and pass the minimal quality checks. 
To ease these tasks, you can use the included [makefile](../Makefile) is included if `make` tool installed on your machine. If you do not have `make`, you can just inspect the [makefile](../Makefile) and perform the action included in its targets :-)

1. Make sure you run in activated virtual environment; to refresh your environment, do
```sh
# clean all the artifacts including the virtsula environment
make clean-all

# make sure python version is `3.12`
$ which python
$ python --version

# create virtual environment
$ python -m venv .venv

# activate new virtual environment 
#
# on Linux:
$ . .venv/bin/activate 
#
# on Windows:
$ . .venv/Scripts/activate 

# update pip
$ python.exe -m pip install --upgrade pip
```

2. Install the project in the developement mode; this can take time as it installs GIN with its many dependencies.
```sh
$ make install-dev
``` 

3. After making the changes, do quality checks and fixes:
```sh
$ make ruff   # fix reported issues
$ make black  # run to see formatting needed
$ make fmt    # do format if needed

# now do the whole check with
$ make check
```

4. Now you can commit and push your changes :-)