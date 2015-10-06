These all are valid in Pycharm and running commands use terminal of pycharm(for easyness)

1.first install pip
sudo apt-get install python-pip

2.than install virtual eneviornment
pip install virtualenv


3.now go to setting-> project->project interpreter ->create a virtual eviornment and try to put the folder in in project itself .its easy to see and track .if only there is one enviornment is going to use it .

4.{$EnviornmentName}/bin/pip install -r path/to/requirements.txt

5.on run Configuration set runserver.py as a script and for interpreter project default(your enviornment)