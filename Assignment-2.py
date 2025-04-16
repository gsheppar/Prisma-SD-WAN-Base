#!/usr/bin/env python3
import prisma_sase
import argparse
from prisma_sase import jd, jd_detailed
import sys
import logging
import os
import datetime
import collections
import csv 



# Global Vars
SCRIPT_NAME = 'SDWAN: Example script'
SCRIPT_VERSION = "v1"

# Set NON-SYSLOG logging to use function name
logger = logging.getLogger(__name__)

##############################################################################
# Prisma SD-WAN Auth Token
##############################################################################

sys.path.append(os.getcwd())
try:
    from prismasase_settings import PRISMASASE_CLIENT_ID, PRISMASASE_CLIENT_SECRET, PRISMASASE_TSG_ID

except ImportError:
    PRISMASASE_CLIENT_ID=None
    PRISMASASE_CLIENT_SECRET=None
    PRISMASASE_TSG_ID=None

def get(sase_session):
    
    for sites in sase_session.get.sites().cgx_content['items']:
        tag = None
        if sites["element_cluster_role"] == "SPOKE":
            tag = "Branch-Site"
        else:
            tag = "Data-Center-Site"
        
        
        #### Your Code Goes Here #####
    
        print("You should have removed this section with your code ")
        return
    
        ##############################
        
    return

                                          
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################

    
    sase_session = prisma_sase.API()
    sase_session.set_debug(0)

    sase_session.interactive.login_secret(client_id=PRISMASASE_CLIENT_ID,
                                          client_secret=PRISMASASE_CLIENT_SECRET,
                                          tsg_id=PRISMASASE_TSG_ID)
    if sase_session.tenant_id is None:
        print("ERR: Login Failure. Please provide a valid Service Account")
        sys.exit()
    

    get(sase_session)
    
    # end of script, run logout to clear session.

if __name__ == "__main__":
    go()