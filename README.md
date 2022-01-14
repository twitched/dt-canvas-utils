# Useful Canvas Utitities

A bunch of useful canvas utitities that I use in my classes at Boise State University

## Install on Mac

1. Install python and the latest git

    `brew install python3, git, visual-studio-code`

2. Clone the git repository

    `git clone https://github.com/twitched/dt-canvas-utils.git`

3. Complete the common installation steps below

## Install on Windows

1.  [Download and Install Python](https://www.python.org/downloads/) and choose the folloing
    1.  Install the "py launcher" 
    2.  Associate files with python
    3.  Add Python to environment variables
   
3.  [Donwload the utilities as a zip file](https://github.com/twitched/dt-canvas-utils/archive/refs/heads/main.zip)
4.  Unzip them into an appropriate folder
5.  Complete the common installation steps below
   
## Common Installation Steps

1.  Install the neede python packages from the command line (I suggest Windows Terminal instead of cmd.exe)

    `pip3 install canvasapi keyring`

2.  Get your Canvas API credentials
    1.  Login to Canvas
    2.  Go to Account → Settings
    3.  Under Approved Integrations, click "New Token"
    4.  Give it any purpose.  No expiration necessary
    5.  Either leave the browser window open or copy the token to a secure document
3.  At the command line put your secrets in the credential storage

    1. Enter the canvas url (https://your.canvas.server/)

        `keyring set canvas url`

    2. Enter the canvas token (the token you just generated above)
   
        `keyring set canvas token`
    
4.  You are now ready to use the utilities.  Test it using in the directory containin the utilities

        python3 testapi.py