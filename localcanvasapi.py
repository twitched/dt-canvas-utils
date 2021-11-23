import argparse, keyring
from canvasapi import Canvas

# Read the URL and KEY from a file and create and return a Canvas API object
def startcanvasapi(args: argparse.Namespace) -> Canvas:
    # Canvas API URL
    secrets = {}
    if(args and args.secrets):
        secrets = read_secrets(args.secrets)
    else:
        secrets['CANVAS_API_URL'] = keyring.get_password("canvas", "url")
        secrets['CANVAS_API_KEY'] = keyring.get_password("canvas", "token")   
    return Canvas(secrets['CANVAS_API_URL'], secrets['CANVAS_API_KEY'])

def read_secrets(secrets_file: str) -> dict:
    secrets_dict = {}
    secrets_file = open(secrets_file, 'r')
    for line in secrets_file:
        key, value = line.split('=')
        secrets_dict[key.strip()] = value.strip() 
    return secrets_dict   
    
def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--secrets',
                    help='the file containing the API URL and key.  If not present, will look for it using keyring at "canvas", "token" and "url"')
    return parser

# Set logging to debug
def debug():
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)