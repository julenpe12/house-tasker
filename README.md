# house-tasker
A Django project that helps day-to-day life. Made to be hosted in embeded systems.

# Create enviornment
## Linux
```bash
# Install Python venv and activate
sudo apt install python3.10-venv
sudo python -m venv htenv
source htenv/bin/activate
```
## Windows
### Non superuser
```bash
# Change path of projects and env to C:/User/ and check changes
set WORKON_HOME = %USERPROFILE%/Envs
echo %WORKON_HOME%

# Create env and activate
pip install virtualenvwrapper-win
cd %USERPROFILE%/Envs
mkvirtualenv htenv
workon htenv
```
### Superuser
TODO

# Install Django
```bash
pip install django

# To process user profile images we need Pillow
python -m pip install Pillow
```
