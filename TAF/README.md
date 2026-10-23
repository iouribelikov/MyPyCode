# Installation
## Create a virtual environment
### Option 1 -- using ‘conda‘
To create the virtual environment configured in the file ‘taf_env.yml‘, one simply needs
to run:
‘‘‘
conda env create -f taf_env.yml
'''
*Note: to update an existing virtual environment (if one wished to modify ‘taf_env.yml‘),
run:*
‘‘‘
conda env update --name taf_env --file taf_env.yml --prune
‘‘‘
### Option 2 -- using python ‘venv‘
To create a virtual environment named ‘taf_env‘ with version 3.12 (this is an example) of
Python, run:
‘‘‘
python3.12 -m venv taf_env
‘‘‘
*Careful: you have to choose the right location on your computer, because the files
associated to this virtual environment will be created at this location.*
Once the environment is created, you can enter it via:
‘‘‘
TAF course (Preliminary)- October 8, 2026
source path/taf_env/bin/activate
‘‘‘
Once inside this environment, **and only once inside (!)**, run:
‘‘‘
pip install --upgrade pip
python3 -m pip install -r requirements_py_venv_taf.txt
‘‘‘
to install the requirements defined in the file ‘requirements_py_venv_taf.txt‘

## Python path to ‘Utils‘ modules
In order to be able to easily import TAF ‘Utils‘ modules in local scripts, a solution is
to add the following line to your ‘~/.bashrc‘ or ‘~/.bash_profile‘:
‘‘‘
export PYTHONPATH="${PYTHONPATH}:${TAF}/Utils"
‘‘‘
*Note: doing so, we will not need to specify the path of the module relative to the
script we are developping.*
*Careful: do not forget to either open a new terminal or to ‘source‘ your ‘bash*‘ file to
make this modification active.*

