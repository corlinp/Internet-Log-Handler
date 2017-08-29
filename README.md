# Internet Log Handler

Internet Log Handler for python is a work in progress. Essentially it
will provide a Python logging handler (already done, ilog.py) that sends
all your logs up to a server, and a corresponding tornado server and web
page that allows you to monitor your logs in real time (over WebSockets).
Currently __init__.py does contain a Flask server for simple HTTP hosting
of logs.