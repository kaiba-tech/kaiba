# Version history

| Change | Bumps |
| - | - |
| Breaking | major |
| New Feature | minor |
| otherwise | patch |


## Version 1.0.0 Release: Kaiba

Kaiba is a data transformation tool written in Python that uses a DTL(Data Transformation Language) expressed in normal JSON to govern output structure, data fetching and data transformation.

### Features

* Mapping by configuration File.
* Looping/Iterating data from multiple places to create 1 or many objects
* Combine multiple values to one.
* Default values
* If statements
    * conditions: is, not, in, contains
    * can match any valid json value including objects and lists
* Casting
    * integer, decimal, iso date
* Regular Expressions
    * get whole regex result
    * choose matching groups
* Slicing
    * Slice/Substring strings or arrays

### Changelog

* Restructures pydantic models
* Rename Mapping->DataFetcher
* Rename Attribute.mappings->Attribute.data_fetchers
* Rename Regexp->Regex
* Rename Regex.search to Regex.expression
* Rename Iterable->Iterator
* Rename iterables->iterators
* Simplify typing


## Version 0.3.0 - Migrate to pydantic

This version changes how we validate our json configuration and also how we parse it. Using pydantic it is much easier to handle to handle typing and the code in general.

* Removes json schema adds pydantic for config validation

## Version 0.2.1 - Schema troubles

Kaiba is forked from the greenbird/piri @ version 2.2.0

Fixes problems with Schema validation

* In attribute make sure either name + mappings or name + default is required
* In mappings make sure that length of path is above 1 if default is not provided.
