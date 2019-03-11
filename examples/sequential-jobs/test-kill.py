import signal
import time



class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        # signal.signal(signal.SIGKILL, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

killer = GracefulKiller()
counter = 0
while(True):
    print("I am still alive ...")
    if killer.kill_now:
        print("recieve kill signal.")
    time.sleep(1)
    counter += 1
    if counter > 60:
        break


#  Command to kill a process is : timeout -k <buffer window> <time> <command...>
