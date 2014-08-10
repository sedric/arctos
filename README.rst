arctos
======

Arctos is a simple message server using HTTP.

It's all about sending messages and recieve them on a channel.

A channel is the "path" part of the URL.

How do I launch it?
===================

We have two scripts.

arctos, the server. You can just launch it and it will works, but you may
want to customize it, you can get all the options you need with --help :

::

  ./arctos.py --help
  usage: arctos.py [-h] [-i I] [-p P]

  Messaging HTTP server

  optional arguments:
    -h, --help  show this help message and exit
    -i I        Interface used (default : all)
    -p P        Port used for listen (default : 8080)

arctosd, wich is a tool to launch arctos as a daemon.

::

  ./arctosd.py --help
  usage: arctosd.py [-h] [-p P] [-i I] [--pid PID] [--user USER] [--group GROUP]

  Messaging HTTP daemon

  optional arguments:
    -h, --help     show this help message and exit
    -p P           Port used for listen (default : 8080)
    -i I           Interface used (default : all)
    --pid PID      where the pid file should be placed (default :
                   /var/run/arctosd.pid
    --user USER    Change to user when daemonize (default : nobody)
    --group GROUP  Change to group when daemonize (default : nogroup)


How do I use it?
================

If I want to send "bar" on the channel "foo", I just have to POST it :

::

      $ wget http://localhost:8080/foo --post-data="bar" -q

Now, if I want to check if I had a message on the channel foo, I'll juste have
to GET it.

::

     $ wget http://localhost:8080/foo -qO-
     bar

Simple.

When you request data, the server will always make you wait for fresh data,
unless you specify you don't want to :

::

   $ wget http://localhost:8080/foo?last -qO-

If there is no data awailable, it will return a 404 error and no data.
