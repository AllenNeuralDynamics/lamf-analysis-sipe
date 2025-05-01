# Welcome

lamf-analysis is a sandbox/development repo for ophys and behavior processing and analysis.

**Projects:** Mostly created for learning and mFISH, but may work with omFISH and U01.

## Installation

**Code ocean capsule**
Add these lines to a code ocean capusle docker file
```
 RUN git clone https://github.com/AllenNeuralDynamics/lamf-analysis \
    && cd lamf_analysis \
    && pip install -e .
```

## Executable
This library can be bundled as an executable. Github actions should be enabled for this repository to build it on pushes to main. To build locally (only tested on windows 10 with anaconda and python 3.10.9 installed).

Initialize build environment (may need to be called 2x)
```bash
init_build_env
```

Build executable
```bash
build_exe
```

Build debug executable (console logs will get displayed)
```bash
build_debug_exe
```

### Testing the executable

Expected testing environment (mocking mesoscope workflow environment as of 04/30/2025):

- python 3.9.5
- windows 10 operating system
- pydantic-settings

Parametrization is determined via `pydantic-settings`, so a `.env` file can be used to further parametrize tests.

To run all tests

```bash
test_local_zstack_sort
```

To run just mypy tests

```bash
test_local_zstack_sort --only_mypy
```

## Contributing
+ Make a PR, tag a reviewer




