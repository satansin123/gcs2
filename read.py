def readfromback(filename):
    with open(filename) as csv :
        lines = csv.readlines()
        for line in reversed(lines):
            array = [int(string) for string in line.rstrip('\n').split(",")]
            yeild(array)
