import sys
import pandas as pd

'''
expect 2 command-line arguments, in addition to name of file (analysis.py).
should be able to convert both from strings to times. 
second time should be after the first.
'''
def validate_input(): 
    if len(sys.argv) != 3: 
        raise ValueError("Incorrect Number of Command Line Arguments. Expected 3, received: ", len(sys.argv))

    try: 
        time1 = pd.to_datetime(sys.argv[1], format="%Y-%m-%d %H")
    except: 
        raise ValueError("First Argument Should be Date String Formatted as YYYY-MM-DD HH, Recieved: ", sys.argv[1])

    try: 
        time2 =  pd.to_datetime(sys.argv[2], format="%Y-%m-%d %H")
    except: 
        raise ValueError("Second Argument Should be Date String Formatted as YYYY-MM-DD HH. Received: ", sys.argv[2])

    if time1 >= time2: 
        raise ValueError("End Hour Should be After Start Hour. Provided Start Hour: ", sys.argv[1], ". Provded End Hour: ", sys.argv[2])
    
    return time1, time2