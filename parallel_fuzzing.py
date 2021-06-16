import os
import time
import sys

__author__ = "Samuel K."
__credits__ = ["Samuel K.", "Tobias S."]
__version__ = "0.2"
__maintainer__ = "Samuel K."
__status__ = "Development"

# check for valid arguments
if len(sys.argv) == 1:
    threads = 1
else:
    try:
        threads = int(sys.argv[1])
    except ValueError:
        print('wrong argument', file=sys.stderr)
        exit(1)

# TODO argv parser
outName = "program"
inFolder = "in"
outFolder = "out"

# exit program when thread count is too low
if threads < 1:
    print("Thread count is too low.", file=sys.stderr)
    exit(2)

# clear fuzzer output folder if exists
if os.path.isdir(outFolder): os.popen("rm -r", outFolder)

# compile server files
os.popen("afl-clang -g *.c -o " + outName + " -lmagic -lm -lcrypto")
time.sleep(0.5)

# spawn master fuzzer
os.popen("AFL_NO_UI=1 afl-fuzz -i in -o " + outFolder + " -M master ./" + outName + " stdin")

# spawn slave fuzzers
if threads >= 1:
    time.sleep(2)
    for i in range(0, threads-1):
        os.popen("AFL_NO_UI=1 afl-fuzz -i in -o " + outFolder + " -S fuzzer" + str(i) + " ./" + outName + " stdin")

# main loop for overview and exiting
try:
    time.sleep(1)
    while True:
        i = input("\"Overview\" or \"exit\"\n").lower()
        if i == "overview":
            print(os.system("afl-whatsup parallelfuzzOut"))
        elif i == "exit":
            os.popen("pkill -f afl")
            os._exit(0)
            break
        else:
            print("input not implemented", file=sys.stderr)
except KeyboardInterrupt:
    os.popen("pkill -f afl")
    print("Fuzzing stopped by user.", file=sys.stderr)
