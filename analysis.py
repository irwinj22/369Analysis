import time
import sys
import csv

# to record time elapsed during analysis
start_time = time.perf_counter_ns()

'''
input validation
expect 2 command-line arguments, in addition to name of file (analysis.py).
should be able to convert both from strings to times. 
second time should be after the first.
'''
if len(sys.argv) != 3: 
    raise ValueError("Incorrect Number of Command Line Arguments. Expected 3, received: ", len(sys.argv))

try: 
    time1 = time.strptime(sys.argv[1], "%Y-%m-%d %H")
except: 
    raise ValueError("First Argument Should be Date String Formatted as YYYY-MM-DD HH, Recieved: ", sys.argv[1])

try: 
    time2 = time.strptime(sys.argv[2], "%Y-%m-%d %H")
except: 
    raise ValueError("Second Argument Should be Date String Formatted as YYYY-MM-DD HH. Received: ", sys.argv[2])

if time1 >= time2: 
    raise ValueError("End Hour Should be After Start Hour. Provided Start Hour: ", sys.argv[1], ". Provded End Hour: ", sys.argv[2])

# to store distinct colors, number of appearances in dataset
colors = {}
# to store distinct coords, number of appearances in dataset
coords = {}


with open('2022_place_canvas_history.csv', newline = '') as csvfile: 
    reader = csv.DictReader(csvfile)
    for row in reader: 
        # convert from string to actual time
        if "." in row["timestamp"]: 
            timestamp =  '%Y-%m-%d %H:%M:%S.%f UTC'
        else: 
            timestamp =  '%Y-%m-%d %H:%M:%S UTC'

        current_time = time.strptime(row["timestamp"], timestamp)
        
        # if time is within range, want to account for it.
        if time1 <= current_time <= time2: 
            current_color = row["pixel_color"]
            current_coord = row["coordinate"]
            # if color already seen, add one to number of appearances
            if current_color in colors: 
                colors[current_color] += 1
            # if not, create new entry and set number of appearances to one
            else: 
                colors[current_color] = 1
            # now do the same for coordinates
            if current_coord in coords: 
                coords[current_coord] += 1
            else: 
                coords[current_coord] = 1

max_color = max(colors, key=colors.get)
max_coord = max(coords, key=coords.get)

end_time = time.perf_counter_ns()
elapsed_time = end_time - start_time

print("**TIMEFRAME**: ", sys.argv[1], " to ", sys.argv[2])
print("**EXECUTION TIME:** ", round(elapsed_time / 1000000, 2), " milliseconds")
print("**MOST PLACED COLOR**: ", max_color)
print("**MOST PLACED PIXEL LOCATION**:", max_coord)