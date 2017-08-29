import logging
import requests
from threading import Thread
import atexit

try:
    from Queue import Queue
except: # This means python3
    from queue import Queue



class InternetLogHandler(logging.StreamHandler):
    def __init__(self, password=None):
        self.password = password
        self.q = Queue()
        self.t = Thread(target=self.worker, args=(self.q,))
        self.t.setDaemon(True)
        self.t.start()
        atexit.register(self.join_all)
        logging.StreamHandler.__init__(self)

    def join_all(self):
        self.q.join()


    def worker(self, q):
        while True:
            record = q.get()
            name = record.name
            time = record.created  # unix seconds with decimals
            caller = record.module
            level = record.levelname
            msg = self.format(record)
            out = "%s: %s:    %s" % (caller, level, msg)
            requests.post("http://localhost/"+name, out)
            q.task_done()


    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)
            stream.write('\n')
            self.q.put(record)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


if __name__ == '__main__':
    ez = InternetLogHandler()

    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(ez)

    import time
    for i in range(100):
        time.sleep(1)
        logger.info("This is log number %i."%i)