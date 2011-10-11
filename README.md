Parlamentarier-Buzzwords
========================

Dieses Projekt ist im Rahmen des [Make Open Data Camp 2011](http://makeopendata.ch/) entstanden.
Der Zweck des Projekt ist es, politische Vorstösse von Parlamentariern zu sammeln, zu analysieren,
und die am häufigsten verwendeten Stichworte in einer [Tag Cloud](http://de.wikipedia.org/wiki/Schlagwortwolke)
zu visualisieren.

Screenshot:

![Screenshot](https://raw.github.com/gwrtheyrn/gesagt-im-parlament.ch/master/screenshot_small.png)

Technologie, Aufbau
-------------------

Der Ablauf ist folgendermassen:

  1. Die Daten werden von verschiedenen Quellen geparsed. Momentan wird nur parlament.ch
     berücksichtigt. Die Daten werden mit einem Scala-Script geparsed und dann in ein JSON File
     gespeichert.
  2. Dieses JSON File wird vom Frontend einmalig geparsed und in die Datenbank geschrieben. Das
     Frontend ist in Python / Django geschrieben. Das Parse Script wurde als ./manage.py-Script
     realisiert.
  3. Die Aggregation und Sortierung / Zählung dieser Daten wird momentan on-the-fly durchgeführt.

Requirements
------------

  * For the scraping: Scala
  * For the frontend: Python, Django, python-requests

Setup
-----

To setup the Django frontend, it is recommended that you use a python-virtualenv.

  1. Activate your virtualenv
  2. Install dependencies: `pip install -r requirements.txt`
  3. Run Django server: `./manage.py runserver`

To reparse the data, issue the following commands:

  1. `rm db.sqlite`
  2. `./manage.py syncdb`
  3. `./manage.py parse_affairs`
  4. `./manage.py parse_persons`


License
-------

This code is - unless noted otherwise - distributed under a BSD like license.
