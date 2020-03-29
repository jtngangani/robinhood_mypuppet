# robinhood-mypuppet
Tool to source protfolio data from robinhood into spreadsheet/csv

############  How to clone ############:
 > git clone https://github.com/jtngangani/robinhood_mypuppet.git
 
############  How to setup ############

1. Create VirtualEnv
   > mkdir venv_dir
   
   > cd venv_dir
   
   > python3 -m venv robinhood_mypuppet_venv
   
   > source robinhood_mypuppet_venv/bin/activate

change directory to 
  > cd robinhood_mypuppet/

2. Install dependencies
  > pip install -r requirements.txt
 
########### How to run #################

1. Before running, (optional) populate username and password in credential.txt
   If you dont populate in the file, It would ask you to enter on prompt

2. usage: my_rh.py [-h] [--dump_portfolio] [--dump_transactions]

    The script reads RH credentials from credentials.txt and takes appropriate
    action depending on following args

    optional arguments:
      -h, --help           show this help message and exit
      --dump_portfolio     Dumps portfolio into pf_rh.csv
      --dump_transactions  Dumps transactions history

      Ex: python my_rh.py --dump_portfolio ## This dumps the portfolio in rh_pf.csv
