# Experiment 1: `csvkit` and the Consolidated Screening List

## Get oriented

First, what is the scale of the data we're dealing with? Just how long is the
Consolidated Screening List? We can find out with `wc -l`:

```shell
$ cat data/csl/consolidated_party_list_final.csv | wc -l
   28729
```

> `wc` stands for "word count"; the `-l` option tells it to count lines instead.

Woah, more than 28000 lines. We probably don't want to look at them all
every time, so let's take a peek at the first five lines with
`head -n 5`:

```shell
$ head -n 5 data/csl/consolidated_party_list_final.csv
"Last updated: May 23, 2014",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Source List,Entity Number,SDN Type,Programs,Name,Title,Address,City,State/Province,Postal Code,Country,Federal Register Notice,Effective Date,Date Lifted/Waived/Expired,Standard Order,License Requirement,License Policy,Call Sign,Vessel Type,Gross Tonnage,Gross Register Tonnage,Vessel Flag,Vessel Owner,Remarks/Notes,Address Number,Address Remarks,Alternate Number,Alternate Type,Alternate Name,Alternate Remarks,Web Link
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,13th Institute China Aerospace Times Electronics Corp (CATEC),,http://www.bis.doc.gov/entities/default.htm
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,713 Institute of Beijing,,http://www.bis.doc.gov/entities/default.htm
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,Beijing Aerospace Control Instruments Institute,,http://www.bis.doc.gov/entities/default.htm
```

We could also do this by piping the file to `head`, of course:
```shell
$ cat data/csl/consolidated_party_list_final.csv | head -n 5
```
This tells us that the first row is **not** the column names, as we might expect.

Get rid of that extra line with `sed`:

```shell
$ cat data/csl/consolidated_party_list_final.csv | head -n 5 | sed "1d"
Source List,Entity Number,SDN Type,Programs,Name,Title,Address,City,State/Province,Postal Code,Country,Federal Register Notice,Effective Date,Date Lifted/Waived/Expired,Standard Order,License Requirement,License Policy,Call Sign,Vessel Type,Gross Tonnage,Gross Register Tonnage,Vessel Flag,Vessel Owner,Remarks/Notes,Address Number,Address Remarks,Alternate Number,Alternate Type,Alternate Name,Alternate Remarks,Web Link
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,13th Institute China Aerospace Times Electronics Corp (CATEC),,http://www.bis.doc.gov/entities/default.htm
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,713 Institute of Beijing,,http://www.bis.doc.gov/entities/default.htm
EL,,,,"13 Institute, China Academy of Launch Vehicle Technology (CALT)",,,,,,China,66 FR 24265,05/14/2001,,,For all items subject to the EAR (See ?744.11 of the EAR),See ?744.3(d) of this part,,,,,,,,,,,,Beijing Aerospace Control Instruments Institute,,http://www.bis.doc.gov/entities/default.htm
```

> `sed` stands for "stream editor". `"1d"` means "delete line 1".

## Figure out the columns

Now let's figure out what the columns are with `csvcut`:

```shell
$ cat data/csl/consolidated_party_list_final.csv | head -n 5 | sed "1d" | csvcut -n
  1: Source List
  2: Entity Number
  3: SDN Type
  4: Programs
  5: Name
  6: Title
  7: Address
  8: City
  9: State/Province
 10: Postal Code
 11: Country
 12: Federal Register Notice
 13: Effective Date
 14: Date Lifted/Waived/Expired
 15: Standard Order
 16: License Requirement
 17: License Policy
 18: Call Sign
 19: Vessel Type
 20: Gross Tonnage
 21: Gross Register Tonnage
 22: Vessel Flag
 23: Vessel Owner
 24: Remarks/Notes
 25: Address Number
 26: Address Remarks
 27: Alternate Number
 28: Alternate Type
 29: Alternate Name
 30: Alternate Remarks
 31: Web Link
```

## Deal with encoding issues

Let's inspect just columns 1 and 11 to see list and country:
```shell
$ cat data/csl/consolidated_party_list_final.csv | head -n 5 | sed "1d" | csvcut -c 1,11
Source List,Country
Your file is not "utf-8" encoded. Please specify the correct encoding with the -e flag. Use the -v flag to see the complete error.
```

Oops. Looks like it's not Unicode. Trial end error results in a valid guess
that it's `latin-1` [encoded](http://csvkit.readthedocs.org/en/0.7.3/scripts/common_arguments.html#examples).

Try again:
```shell
$ cat data/csl/consolidated_party_list_final.csv | head -n 5 | sed "1d" | csvcut -c 1,11 -e latin-1
Source List,Country
EL,China
EL,China
EL,China
```

So our first three entries are all from China.

## More statistics

But what does "EL" mean? For that, we have to look at the government's [download instructions](http://export.gov/static/cl_downloading_instructions_08102011_gh_Latest_eg_main_040971.pdf), which say:

> Field Name  |Description
> ------------|-------------
> Source List |3-position code describing the source (agency or agency list) of the record (DPL= Denied Persons List, UVL= Unverified List, EL=Entity List, SDN= Specially Designated Nationals, DTC= AECA Debarred List, ISN= Nonproliferation Sanctions)

So now we know those three Chinese entries are from the [Entity List](http://www.bis.doc.gov/entities/default.htm).

Let's find out more about where these entries are all from, using `csvstat`.
This time let's process the full list (by omitting the call to `head`):

```shell
$ cat data/csl/consolidated_party_list_final.csv | sed "1d" | csvcut -c 1,11 -e latin-1 | csvstat
  1. Source List
	<type 'unicode'>
	Nulls: False
	Unique values: 6
	5 most frequent values:
		SDN:	25454
		EL:	1766
		DTC:	523
		DPL:	474
		ISN:	462
	Max length: 3
  2. Country
	<type 'unicode'>
	Nulls: True
	Unique values: 188
	5 most frequent values:
		Colombia:	3384
		Mexico:	2502
		Kuwait:	2485
		Iran:	1397
		Pakistan:	1128
	Max length: 33

Row count: 28727
```

Now we're getting some interesting data. Just looking at these two columns,
it looks like our initial inquiries were a fluke. The lists are dominated not
by China, but by Colombia, Mexico, and some countries in the Middle East. Also,
the Entity List has just 1766 entries, but the SDN, or
Specially Designated Nationals list, has more than 25000. The SDN is a list
provided by the [Office of Foreign Assets Control](http://www.treasury.gov/about/organizational-structure/offices/Pages/Office-of-Foreign-Assets-Control.aspx) within the US Treasury.

## Let's find out about ships!

What's are the most common names of ships on the SDN? To find out, we'll
chain `csvcut`, `csvgrep`, and `csvstat` together.
1. Use `csvcut` to select columns (Select Source List, SDN Type, Name, and Vessel Flag): `csvcut -e latin-1 -c 1,3,5,22`
2. Use `csvgrep` to search for just vessels, in the SDN Type column: `csvgrep -c 2 -m vessel`
3. Use `csvstat` again to show statistics.

```shell
$ cat data/csl/consolidated_party_list_final.csv | sed "1d" | csvcut -e latin-1 -c 1,3,5,22 | csvgrep -c 2 -m vessel | csvstat
  1. Source List
	<type 'unicode'>
	Nulls: False
	Values: SDN
  2. SDN Type
	<type 'unicode'>
	Nulls: False
	Values: vessel
  3. Name
	<type 'unicode'>
	Nulls: False
	Unique values: 239
	5 most frequent values:
		DORITA:	5
		CATALINA:	4
		PARMIS:	4
		SAVIZ:	4
		HONESTY:	3
	Max length: 21
  4. Vessel Flag
	<type 'unicode'>
	Nulls: True
	Unique values: 17
	5 most frequent values:
		None Identified:	84
		Iran:	78
		Tanzania:	36
		Bolivia:	34
		Hong Kong:	28
	Max length: 15

Row count: 374
```

There's some irony: the fifth most common ship name on the SDN is *Honesty*.

Where is the *Honesty* from? We can further `csvgrep` the Name column to find out:
```shell
$ cat data/csl/consolidated_party_list_final.csv | sed "1d" | csvcut -e latin-1 -c 1,3,5,22 | csvgrep -c 2 -m vessel | csvgrep -c 3 -m HONESTY
Source List,SDN Type,Name,Vessel Flag
SDN,vessel,HONESTY,None Identified
SDN,vessel,HONESTY,None Identified
SDN,vessel,HONESTY,None Identified
```

Oops, actually we can't; there's no flag country listed for any of the
*Honesty* entries. Let's add some more columns. Let's try Vessel Type
(column 19), Call Sign (column 18), Vessel Owner (column 23), and Programs (column 4):
```shell
$ cat data/csl/consolidated_party_list_final.csv | sed "1d" | csvcut -e latin-1 -c 1,3,5,22,19,18,23,4 | csvgrep -c 2 -m vessel | csvgrep -c 3 -m HONESTY
Source List,SDN Type,Name,Vessel Flag,Vessel Type,Call Sign,Vessel Owner,Programs
SDN,vessel,HONESTY,None Identified,Crude Oil Tanker,T2DZ4,,IRAN
SDN,vessel,HONESTY,None Identified,Crude Oil Tanker,T2DZ4,,IRAN
SDN,vessel,HONESTY,None Identified,Crude Oil Tanker,T2DZ4,,IRAN
```

Now we know the *Honesty* is a crude oil tanker with the call sign T2DZ4, and
is linked to Iran somehow. With a little Googling, we can find out all kinds
of interesting stuff about this vessel!
* It bounces back between the ports at [Kharg Island](http://en.wikipedia.org/wiki/Kharg_Island), Iran and [Zhoushan](http://en.wikipedia.org/wiki/Zhoushan#Economy), China
* Latest info: [*Honesty* on MarineTraffic.com](http://www.marinetraffic.com/ais/details/ships/9357391/vessel:HONESTY?lang=pl)

## Well, that's weird

But why is the *Honesty* listed three times? Let's look again at the raw data, all columns:

```shell
$ cat data/csl/consolidated_party_list_final.csv | sed "1d" | csvgrep -m HONESTY -c 5 -e latin-1
Source List,Entity Number,SDN Type,Programs,Name,Title,Address,City,State/Province,Postal Code,Country,Federal Register Notice,Effective Date,Date Lifted/Waived/Expired,Standard Order,License Requirement,License Policy,Call Sign,Vessel Type,Gross Tonnage,Gross Register Tonnage,Vessel Flag,Vessel Owner,Remarks/Notes,Address Number,Address Remarks,Alternate Number,Alternate Type,Alternate Name,Alternate Remarks,Web Link
SDN,15056,vessel,IRAN,HONESTY,,,,,,,,,,,,,T2DZ4,Crude Oil Tanker,"317,356","163,660",None Identified,,Former Vessel Flag Cyprus; alt. Former Vessel Flag Tuvalu; alt. Former Vessel Flag Tanzania; Vessel Registration Identification IMO 9357391; MMSI 572450210; Linked To: NATIONAL IRANIAN TANKER COMPANY.,22392,,22165,fka,HIRMAND,,http://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/default.aspx
SDN,15056,vessel,IRAN,HONESTY,,,,,,,,,,,,,T2DZ4,Crude Oil Tanker,"317,356","163,660",None Identified,,Former Vessel Flag Cyprus; alt. Former Vessel Flag Tuvalu; alt. Former Vessel Flag Tanzania; Vessel Registration Identification IMO 9357391; MMSI 572450210; Linked To: NATIONAL IRANIAN TANKER COMPANY.,22392,,23483,fka,HONESTY,,http://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/default.aspx
SDN,15056,vessel,IRAN,HONESTY,,,,,,,,,,,,,T2DZ4,Crude Oil Tanker,"317,356","163,660",None Identified,,Former Vessel Flag Cyprus; alt. Former Vessel Flag Tuvalu; alt. Former Vessel Flag Tanzania; Vessel Registration Identification IMO 9357391; MMSI 572450210; Linked To: NATIONAL IRANIAN TANKER COMPANY.,22392,,24782,fka,MILLIONAIRE,,http://www.treasury.gov/resource-center/sanctions/SDN-List/Pages/default.aspx
```

Flipping between this and the column descriptions, we can see that columns 28
and 29 hold the answer. Column 28 for each says "fka" and Column 29 has a
different name in each of the three rows: "HIRMAND", then "HONESTY", then
"MILLIONAIRE". This tells us that there are three rows because the ship has
had multiple former names, **two of which are pretty awesome**.
