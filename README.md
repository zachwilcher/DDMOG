# How the project was set up

A conda environment is created with
```bash
conda env create --prefix .conda-env -f conda-environment.yml
```

The environment can be activated with
```bash
conda activate ./.conda-env
```

If the environment needs to be updated, edit the `conda-environment.yml` file and run
```bash
conda env update --prefix .conda-env -f conda-environment.yml --prune
```
