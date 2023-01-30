with open("data/100DayLog.txt", "w+") as logFile:
    for x in range(1, 101):
        logFile.write(f"### Day {x}: \n**Today's Progress:** \n\n**Thoughts:**\n\n")
    logFile.close()
