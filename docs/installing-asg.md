# Installing the ASG

## Clone the repository

```sh
git clone https://gitlab.teadal.ubiwhere.com/teadal-tech/asg_generation_code.git <folder_name>
cd <folder_name>
```

## Create virtual environment with `python3.12`

- make sure python version is `3.12`
```sh
$ which python
$ python --version
```
- create and activate virtual environment
```sh
$ python -m venv .venv
$ . .venv/Scripts/activate  # on Windows
$ . .venv/bin/activate      # On Linux
```

- validate the activation 
```sh
$ which python  # should point to python binary inside the virtual environment
$ which pip     # should point to pip binary inside the virtual environment
```

- upgrade pip
```sh
$ python -m pip install --upgrade pip
```

## Install runtime dependencies
```sh
$ python -m pip install -r .reqs/requirements.txt
```

On Windows, the following problem can occur. The solution  is described [here](https://stackoverflow.com/questions/73969269/error-could-not-build-wheels-for-hnswlib-which-is-required-to-install-pyprojec/76245995#76245995).
```sh
...
Building wheels for collected packages: chroma-hnswlib
  Building wheel for chroma-hnswlib (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Building wheel for chroma-hnswlib (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [5 lines of output]
      running bdist_wheel
      running build
      running build_ext
      building 'hnswlib' extension
      error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for chroma-hnswlib
Failed to build chroma-hnswlib
ERROR: Failed to build installable wheels for some pyproject.toml based projects (chroma-hnswlib)
```


export 