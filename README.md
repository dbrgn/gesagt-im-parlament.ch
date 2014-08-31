Parlamentarier-Buzzwords
========================

Dieses Projekt ist im Rahmen des [Make Open Data Camp 2011](http://makeopendata.ch/) entstanden.
Der Zweck des Projekt ist es, politische Vorstösse von Parlamentariern zu sammeln, zu analysieren,
und die am häufigsten verwendeten Stichworte in einer [Tag Cloud](http://de.wikipedia.org/wiki/Schlagwortwolke)
zu visualisieren.

Screenshot:

![Screenshot](https://raw.github.com/dbrgn/gesagt-im-parlament.ch/master/screenshot_small.png)

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
  3. Create database: `./manage.py syncdb`
  4. Run Django server: `./manage.py runserver`

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

If you have a previous database with councillor information that isn't available in the new database
(e.g. because they weren't elected anymore), you can import the data using the command:

  6. `./manage.py merge_oldpersons`

The command assumes that your old database is a postgresql database called 'Parlament'. If not,
edit the script directly.

License
-------

This code is - unless noted otherwise - distributed under a BSD like license.

Media mentions
--------------

 * 28.06.12 [Open Government Data Studie Schweiz](http://www.zora.uzh.ch/63318/1/20120628093057_merlin-id_7116.pdf)
 * 05.06.12 [Digitale Gesellschaft](http://www.digitale-gesellschaft.ch/2012/06/05/opendata-ch-konferenz-projekte/)
 * 28.05.12 [Beitrag auf Politnetz](http://www.politnetz.ch/beitrag/14675)
 * 09.05.12 [BILAN](http://www.bilan.ch/articles/techno/la-suisse-va-t-elle-laisser-l%E2%80%99economie-surfer-sur-ses-donnees)
 * 01.04.12 [infoblog.li](http://infoblog.li/innovation-auf-basis-von-open-data/)
 * 30.01.12 [itopia](http://www.itopia.ch/repository/Publikationen/120130\_SGVW\_fokusartikel-OGD\_definitiv.pdf)
 * 23.10.11 [philippkueng.ch](http://philippkueng.ch/makeopendatach-2011.html)
 * 17.10.11 [Telepolis](http://www.heise.de/tp/blogs/4/150631)
 * 12.10.11 [datavisualization.ch](http://datavisualization.ch/events/review-of-switzerlands-first-open-data-camp/)
 * 07.10.11 [IFI Uni Zürich](http://www.ifi.uzh.ch/ddis/news/opendataparliment.html)
