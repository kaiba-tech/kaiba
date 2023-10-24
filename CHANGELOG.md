# Version history

| Change | Bumps |
| - | - |
| Breaking | major |
| New Feature | minor |
| otherwise | patch |


## Latest Changes

## Version 3.0.0 @dataclass from attr bug and no more callable objects.

We were using `@dataclass` decorator from attr, which caused kaiba not to run when used in an environment that did not have attr installed. Thanks to @ChameleonTartu for finding and reporting the bug.

Non-private code has been changed which is why this is a major version. In the future we will make sure to have clearer line between what is private internal kaiba code and what is the interface that users will use. 

### Internal

* We are now callable object free. From now on, we will only use functions. 


## Version 2.0.0 Upgrade dependencies, support python 3.10, 3.11

This major version bump was needed because we upgrade `pydantic` to version 2 from version 1. This changed a lot of error messages in schema validation. If anyone was depending on those, it would break their code. In the same update we are updating a lot of other dependencies too. Most importantly going from `returns` 0.14 to 0.22. This might mean we can make the functional code look better in the future. We are also now support python 3.10 and 3.11 and test them like we do 3.8 and 3.9.

### Breaking

* Upgrades to `pydantic` version 2. This is a breaking change because it changes the output of validation errors. 

### Upgrades

* Bumps `returns` to `0.22`

### Internal

* Update `mypy` version
* CI - Github workflow tests now targets `main` branch instead of `master`


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
