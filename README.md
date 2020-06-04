Book Rental Store
========================================

Requirements
---------------
python3.7, python-pip, virtualenv


Application
=========================================

1) First, clone this repository

    git clone http://github.com/ngadakh/bookrentalsystem.git
    cd bookrentalsystem

2) Create and activate virtualenv

    virtualenv env
    
    source env/bin/activate

3) Install all necessary to packages:

    pip install -r requirements.txt

4) Run the application

    python run.py

5) To see application access below URL in browser
    http://localhost:5000/login


Tests
============================================
1) How to run tests?

    cd bookrentalsystem
    
    pytest -v

2) How to run coverage?

    coverage run -m pytest
    
    coverage report
    
    coverage html

==============================================

All configuration is in: config.py

For Development use ENVIRONMENT = DevelopmentConfig
For Testing use ENVIRONMENT = TestingConfig