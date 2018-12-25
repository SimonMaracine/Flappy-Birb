try:
    open("file.txt", "r")
except Exception:
    print "Could not find file; creating a new one."
    open("file.txt", "w+")
finally:
    data_file = open("file.txt", "r")
    print data_file.read()
