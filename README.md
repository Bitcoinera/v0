**How to install and run:**<br>
 make sure that python3.6 is installed on your system. <br>
 `sudo apt-get install build-essential libssl-dev libffi-dev python-dev`<br>
 install pip:<br>
 `sudo apt install python-pip`
 <br>`sudo apt install -y python3-venv`<br>
 `sudo pip install virtualenvwrapper`<br>
 `vim ~/.bashrc`<br>
 add these lines to the end of the file: <br>
`export WORKON_HOME=$HOME/.virtualenvs`<br>
`export PROJECT_HOME=$HOME/Devel`<br>
`source /usr/local/bin/virtualenvwrapper.sh`
run <br>
`source ~/.bashrc`<br>
`mkvirtualenv --python=/usr/bin/python3.6 d_tail`<br>
`cd v0`<br>
``


