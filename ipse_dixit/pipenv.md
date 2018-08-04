<< [go back](https://apiraino.github.io)

## On managing Python packages with `pipenv` instead of `pip`+`virtualenv`

Pipenv: [https://docs.pipenv.org](https://docs.pipenv.org)

Pipenv automatically creates a virtualenv, downloads the python version you're interested in, all in two commands. It is the recommended package manager, due to replace `pip`.

Before, I've been installing python version with `pyenv`:
``` bash
$ pyenv install 3.6.4
$ pyenv install 3.5.4
$ pyenv install 2.7.14
```

Install Pipenv globally:
``` bash
$ sudo -H pip install pipenv
```

Now I can use `pipenv` to install the python version *and* create the virtualenv:
``` bash
$ cd ~/myprojects/prj_name/
$ pipenv --python 2.7
```

A file `Pipfile` is being created:
``` bash
$ cat Pipfile
[dev-packages]
"flake8" = ">=3.3.0,<4"
pytest = "*"
mock = "*"

[packages]
django==2.0

[scripts]
tests = "bash ./run-tests.sh"
```

`[dev-packages]` are for development only (e.g. `mock`, `flake8`, `pytest`, ...), `[packages]` are your project real dependencies and `[scripts]` are script bindings (e.g. to execute commands).

Add project dependencies with `$ pipenv install <pkg_name>` or simply edit `Pipfile`.

If you're migrating from a project using `pip` and the usual `requirements.txt` file, simply use `pipenv install` to automatically read that file, install the packages and create/update the `Pipenv` file.

After having installed all the packages create a `Pipfile.lock` snapshot of the packages installed, each identified by a hash:
``` bash
$ pipenv lock
```

## Links

Command reference: https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-install

<< [go back](https://apiraino.github.io)
