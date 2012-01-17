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

Development
-----------

To setup the Django frontend, it is recommended that you use a python-virtualenv.

  1. Activate your virtualenv
  2. Install dependencies: `pip install -r requirements.txt`
  3. Run Django server: `./manage.py runserver`

Scraping
--------

You need Java, Scala and Maven to run the affair scraper.

  1. `cd scraping/affairs/`
  2. `mvn package`
  3. `cd target/`
  4. `java -cp crawler-0.0.1-SNAPSHOT-jar-with-dependencies.jar ch.makeopendata.scraper.AffairScraper`

If errors occur, they will be written into the `failures.txt` file.

Parsing
-------

To parse the scraped data, issue the following commands:

  1. `rm db.sqlite` (remove old database)
  2. `./manage.py syncdb` (create new database)
  3. `./manage.py parse_affairs path/to/affairs.json` (parse affairs.json)
  4. `./manage.py parse_persons` (fetch person details from parlament.ch webservice)
  5. `./manage.py fetch_photos` (fetch new photos from parlament.ch)

License
-------

This code is - unless noted otherwise - distributed under a BSD like license.
