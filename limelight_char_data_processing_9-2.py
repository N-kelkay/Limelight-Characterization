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
timestamps = [15000, 30500, 65500, 76500, 111900, 121200, 144400, 155900, 179300, 203900, 245100, 256000, 285100, 300200, 321500, 326400, 353100, 359700, 467700, 482300, 506900, 522400, 540800, 547500, 571100, 583700, 607200, 616200, 642200, 652200, 689900, 701100, 727000, 737500, 765300, 768300, 790300, 802100, 829000, 839500, 868600, 877100, 900400, 918300, 930300, 950000, 966900, 975300, 999000, 1012600, 1036400, 1050600, 1098700, 1111600]
#X,Y values of each position in order, in feet
#X is lateral distance, Y is distance in front of camera (and is negated later)
actualXs = [0, 0, -1, 0, 1, -2, -1, 0, 1, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2, -3, -2, -1, 0, 1, 2, 3]
actualYs = [1, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
#Tested angles of target to parallel with camera (is negated later)
actualThetas = [10, 30]
#Timestamps we're ignoring because a 3D pose wasn't generated
ignores = [1, 9, 19, 27, 31, 41, 43, 45]

#Determine actual X,Y,Theta for each location and calculate mean/stdev measured
#X,Y,Theta over NUM_SAMPLES samples
o = open("output.csv", "w")
for i in range(len(timestamps)):
    if i in ignores:
        continue
    timestamp = timestamps[i]
    samples = []
    for j in range(NUM_SAMPLES):
        samples.append(getNextPoseAfterTime(timestamp))
    measuredXs, measuredYs, measuredThetas = [*zip(*samples)] #transpose
    output = [actualXs[i // 2] * 12, -actualYs[i // 2] * 12, -actualThetas[i % 2], \
              stat.mean(measuredXs), stat.stdev(measuredXs), \
              stat.mean(measuredYs), stat.stdev(measuredYs), \
              stat.mean(measuredThetas), stat.stdev(measuredThetas)]
    o.write(",".join(map(str, output)) + "\n")

f.close()
o.close()
