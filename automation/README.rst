Environments Requirement
=========================

OS: Ubuntu 14.04 32 bits

Python: Python 2.7.x

Ostinato: 0.8

Environments Installation
=========================

.. code:: shell

    1. Install python in ubuntu
       sudo apt-get install python
    2. Clone this directory to your <local directory>
    3. export PYTHONPATH="<local directory>" in .bashrc and your current shell.
    4. Install virtualenv :
       pip install virtualenv
       mkdir ~/.virt
       cd ~/.virt
       virtualenv -p python .
       source ~/.virt/bin/activate
    5. Install ostinato
       https://github.com/DeltaNSL/Engineering/blob/master/TrafficGenerator/Ostinato/INSTALL.txt
    5. cd <local directory>
       pip install -r requirments.txt
    6. cd <local directory>/icos
       pytest <script>
       