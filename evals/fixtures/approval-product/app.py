"""Small learning fixture. This is not a production approval system."""
import argparse
import json

def submit(role, text):
    if role != 'participant': raise ValueError('Only participants can submit')
    if not text.strip(): raise ValueError('Proposal text is required')
    return {'status':'submitted','visible_to':['participant','facilitator'],'final':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['submit']);p.add_argument('--role',required=True);p.add_argument('--text',required=True);a=p.parse_args()
    try:print(json.dumps(submit(a.role,a.text)))
    except ValueError as e:p.error(str(e))

if __name__=='__main__':main()
