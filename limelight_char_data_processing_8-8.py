import statistics as stat

#How many time slices from Shuffleboard to average over
NUM_SAMPLES = 15

f = open("raw_data.csv", "r")
f.readline() #ignore the first line (column names)

def getNextPoseAfterTime(timestamp):
    """Keep reading the next line of raw data until time is past the argument
    "timestamp" and the pose at that time exists. Return that pose."""
    #Read until we get a pose at a time after "timestamp"
    while True:
        line = f.readline().strip("\n")
        firstCommaIndex = line.index(",")
        time = int(line[:firstCommaIndex])
        pose = line[firstCommaIndex + 3:-2]
        if not (time < timestamp or pose == "" or \
                pose == '0.0, 0.0, 0.0, 0.0, 0.0, 0.0'):
            break
    #Process and return pose
    pose = pose.split(", ")
    pose = list(map(float, pose))
    pose = [pose[0], pose[2], pose[4]] #[X,Y,Z,pitch,yaw,roll]->[X,Y,Theta]
    return pose

#Times at which a location was recorded (milliseconds)
timestamps = [69960, 85280, 134380, 139810, 187000, 204200, 223760, 241230, 340960, 353840, 365480, 374330, 424390, 433840, 454750, 464970, 502840, 512990, 532870, 544490, 590250, 602140, 613450, 620560, 660390, 679590, 694270, 706360, 745220, 757360, 772690, 788370, 830670, 845200, 854110, 863570, 1025940, 1044200, 1057100, 1061270, 1165990, 1192040, 1204230, 1213090, 1277330, 1287970, 1301880, 1321180, 1371220, 1386060, 1400460, 1415570, 1451430, 1459020, 1467790, 1479110, 1514110, 1531410, 1548650, 1556650, 1627180, 1646530, 1660990, 1669630, 1716160, 1727720, 1740900, 1756020, 1797160, 1811670, 1821740, 1833720, 1869070, 1879300, 1889530, 1900740, 1940820, 1953730, 1963940, 1977750, 2132500, 2150810, 2166050, 2169870, 2226850, 2236350, 2249930, 2257800, 2322050, 2335060, 2347160, 2357070, 2394210, 2406680, 2434400, 2445180, 2470240, 2482840, 2494750, 2508390, 2549900, 2560930, 2570690, 2581680, 2627360, 2638880, 2653360, 2670550]
#X,Y values of each position in order, in feet
#X is lateral distance, Y is distance in front of camera (and is negated later)
actualXs = [0, 0, -1, 0, 1, -2, -1, 0, 1, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2, 3]
actualYs = [1, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
#Tested angles of target to parallel with camera (is negated later)
actualThetas = [0, 20, 40, 60]
#Timestamps we're ignoring because a 3D pose wasn't generated
ignores = [2, 3, 7, 10, 11, 15, 22, 23, 27, 31, 38, 39, 43, 47, 58, 59, 62, 63, 66, 67, 71, 82, 83, 86, 87, 106]
#Some 3D poses would only generate if the target was turned past 0 degrees
#Dictionary matches location number to required angle (is negated later)
thetaZeroAdj = {9:10, 10:15, 14:8, 15:12, 16:10, 20:10, 21:15, 22:15}

#Determine actual X,Y,Theta for each location and calculate mean/stdev measured
#X,Y,Theta over NUM_SAMPLES samples
o = open("output.csv", "w")
for i in range(len(timestamps)):
    if i in ignores:
        continue
    timestamp = timestamps[i]
    actualTheta = thetaZeroAdj[i // 4] if i % 4 == 0 and i // 4 in thetaZeroAdj\
                  else actualThetas[i % 4]
    samples = []
    for j in range(NUM_SAMPLES):
        samples.append(getNextPoseAfterTime(timestamp))
    measuredXs, measuredYs, measuredThetas = [*zip(*samples)] #transpose
    output = [actualXs[i // 4] * 12, -actualYs[i // 4] * 12, -actualTheta, \
              stat.mean(measuredXs), stat.stdev(measuredXs), \
              stat.mean(measuredYs), stat.stdev(measuredYs), \
              stat.mean(measuredThetas), stat.stdev(measuredThetas)]
    o.write(",".join(map(str, output)) + "\n")

f.close()
o.close()
