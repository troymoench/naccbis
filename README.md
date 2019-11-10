# Northern Athletics Collegiate Conference Baseball Information System

![Travis-CI Build Status](https://travis-ci.org/troymoench/naccbis.svg?branch=master)

NACCBIS is a baseball information system that provides an analytics solution for teams in the Northern Athletics Collegiate Conference (NACC). The [NACC](http://www.naccsports.org) consists of 12 NCAA Division III colleges and universities from Wisconsin and Illinois. This system is based on the publicly available data found on the [NACC website](http://www.naccsports.org/sports/bsb/2016-17/leaders).

Upon completion, this system will consist of three main components:
1. Web Scraper
2. Data Processor
3. Data Viewer

The following sections detail each of the components

## Web Scraper

The web scraper is a script that programmatically fetches selected raw data from the [NACC website](http://www.naccsports.org/sports/bsb/2016-17/leaders) and exports it in the format of choice. Currently, the only supported formats are CSV and PostgreSQL.

Raw data options include:
1. Individual Offense
2. Individual Pitching
3. Team Offense
4. Team Pitching
5. Team Fielding
6. Game Logs


## Data Processor

The data processor is a script that provides processing and transformation of the raw data. It includes cleansing, assigning player ID's, and advanced metric calculation such as Base Runs and wOBA.

## Data Viewer

The data viewer is a web application that allows users to view and easily interact with the processed data.
