Environments Installation
=========================

.. code:: shell

	  1. Install python in ubuntu
	     sudo apt-get install python
	     
	  2. Clone this directory to your <local directory>
	  
	  3. Set environment variable PYTHONPATH in ~/.bashrc .
	     export PYTHONPATH="<local directory>"
	     
	  4. Install virtualenv
	     pip install virtualenv
	     mkdir ~/.virt
	     cd ~/.virt
	     virtualenv -p python .	     
	     source ~/.virt/bin/activate
	     
	  5. cd <local directory>
	     pip install -r requirment
	     
	  6. cd <local directory>/icos
	     pytest <script>