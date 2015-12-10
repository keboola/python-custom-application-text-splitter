Text splitter
-----------------

Parse data from a SAPI table and split long strings into multiple rows by configurable length.

The output table takes columns text and id specified in the configuration (see below) from the source table and saves them into following columns in the destination table:
- `pk`: Primary key - generated from combination of id and row
- `id`: Copied from id column from the source table (with an optional prefix, configured by idPrefix)
- `row`: Number indicating the part of original string after splitting the original line (starting at 0)
- `text`: The actual row-th part of a source string

Configuration
================

```
{
    "max": 100,
    "min": 50,
    "idPrefix": "",
    "columns": {
        "id": "line_id",
        "text": "split_me"
    }
}
```

- `max`: maximum length of a string to pass / to be cut by the transformation
- `min`: minimum length, if there's no space between max and min, the min value will be used to cut the string off
- `idPrefix`: prefix for the id column
- `columns`:
 - `id`: name of a column containing table row
 - `text`: name of a column with strings to be split by the transformation
Only the specified columns will be downloaded and processed.

Example
==============

### Input data

|"id"|"data"|
|---|---|
|"1"|"Thank you for the amazing service! I'll sure be coming back."|
|"2"|"Hello, are there any actual plans to open a branch of your company anywhere closer to Kamloops? Most of the time it is a pleasure using your services(except for an odd case here and there), however the commute pushes the expenses way above the usual value, not to mention the countless hours spent on the way to you."|
|"3"|"Hello, can you actually clarify how does the price matching work with foreign online stores? You claim you can match 'everyone', does that actually include i.e. european stores?"|

### Configuration

```
{
    "max": 75,
    "min": 50,
    "idPrefix": "",
    "columns": {
        "id": "id",
        "text": "data"
    }
}
```

For configuration in KBC, use [Custom Science Python Application](https://sites.google.com/a/keboola.com/wiki/home/keboola-connection/devel-space/integrating-with-kbc/custom-applications/custom-r-science-applications)
![Configuration screenshot](https://github.com/keboola/python-custom-application-text-splitter/blob/master/doc/screenshot.png)

### Output data

"pk"|"id"|"row"|"text"
---|---|---|---
"1_0"|"1"|"0"|"Thank you for the amazing service! I'll sure be coming back."
"2_0"|"2"|"0"|"Hello, are there any actual plans to open a branch of your company anywhere"
"2_1"|"2"|"1"|" closer to Kamloops? Most of the time it is a pleasure using your"
"2_2"|"2"|"2"|" services(except for an odd case here and there), however the commute"
"2_3"|"2"|"3"|" pushes the expenses way above the usual value, not to mention the"
"2_4"|"2"|"4"|" countless hours spent on the way to you."
"3_0"|"3"|"0"|"Hello, can you actually clarify how does the price matching work with"
"3_1"|"3"|"1"|" foreign online stores? You claim you can match 'everyone', does that"
"3_2"|"3"|"2"|" actually include i.e. european stores?"
