def write_100days():
    logFile = open("100DayLog.txt", "w+")
    for x in range(1, 101):
        logFile.write(f"### Day {x}: \n**Today's Progress:** \n\n**Thoughts:**\n\n")
    logFile.close()

if __name__ == "__main__":
    write_100days()
