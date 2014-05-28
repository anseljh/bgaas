bgaas: Bad Guys As A Service
============================

**Bad Guys As A Service** (`bgaas`) is software for querying export restrictions like
the Denied Persons List.

Installation
------------
Install dependencies:
```shell
$ pip install -r src/requirements.txt
```

Run:
```shell
$ python src/bgaas.py <options> <command> <parameters>
```
Usage
-----
*Note: Most of this is not yet implemented!*

### Update Lists

```shell
$ bgaas update
```

### Query

```shell
$ bgaas query agnese
```
returns results for the query "agnese" from all included lists.

### Map
```shell
$ bgaas map agnese
```

Pronunciation
-------------
The pronunciation of `bgaas` is user selectable: either "bee gas" or "big a**".

License
-------
`bgaas` software and documentation are licensed under the
[Apache License](LICENSE). We make no claim to any data provided by
governments. Some government sample data is included, for testing purposes.

Software
--------
`bgaas` is written in [Python](https://www.python.org/).

Contributing
------------
Pull requests, feature ideas, and bug reports are welcome. You must agree to
license any submitted code under the Apache License or it will be rejected.

The repository is on GitHub at: https://github.com/anseljh/bgaas

To-Do List
----------
* [ ] Parse Consolidated Screening List data file ([instructions](http://export.gov/static/cl_downloading_instructions_08102011_gh_Latest_eg_main_040971.pdf))
* [ ] Document URLs of main raw list data
* [ ] Document update frequency of each main list
* [ ] Document command-line procedures for working with the main arms control [lists](docs/Lists.md) (e.g., with `grep`, `csvkit`)
* [ ] Scrapers for debarment list
    * [ ] Parse Excel file
    * [ ] Parse HTML
* [ ] Scraper for other US lists
* [ ] Identify non-US lists
* [ ] Mapping engine for plotting results, perhaps using [Kartograph](http://kartograph.org/) and [Natural Earth](http://www.naturalearthdata.com/)
* [ ] Write installation instructions

Further Reading
---------------
* [New Media Solutions in Nonproliferation and Arms Control: Opportunities and Challenges](http://www.nonproliferation.org/facebook-youtube-and-the-future-of-nonproliferation/) by Bryan Lee and Margarita Zolotova, published by [The James Martin Center for Nonproliferation Studies](http://www.nonproliferation.org/) (February 14, 2014)
