# Installing the ASG

## Clone the repository from the TEADAL gitlab

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
- create virtual environment
```sh
$ python -m venv .venv
```

## Activate virtual environment 
- on Linux:
```sh
. .venv/bin/activate 
```

- on Windows:
```sh
. .venv/Scripts/activate 
```

## Validate the activation - ensure both `python` and `pip` executables point to binaries inside the virtual environment
```sh
$ which python  
$ which pip    
```

## Upgrade pip
(optional, just to avoid sticky reminders)
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

## Proceed generating the SFDP 

- Configure the ASG and its GIN backend following the instructions [here](./configuring-asg.md) 
- Follow [these instructions](./generating-sfdp.md) to generate the SFDP.