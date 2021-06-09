# Kaiba
Configurable Data Mapping for mortals
___
![test](https://github.com/kaiba-tech/kaiba/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/kaiba-tech/kaiba/branch/master/graph/badge.svg)](https://codecov.io/gh/kaiba-tech/kaiba)
[![Python Version](https://img.shields.io/pypi/pyversions/kaiba.svg)](https://pypi.org/project/kaiba/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
___

**Documentation
([Stable](https://kaiba.readthedocs.io/) |
[Latest](https://kaiba.readthedocs.io/en/latest/)) |
[Source Code](https://github.com/kaiba-tech/kaiba) |
[Task Tracker](https://github.com/kaiba-tech/kaiba/issues)**

## What is Kaiba

Kaiba is a JSON to JSON mapper. That means that we read input JSON and create output JSON. How the output is created is based on instructions from a configuration file. The configuration file governs the the output structure and tells Kaiba where in the input to find data and where to place it in the output. In addition to this Kaiba supports data transformation with `data casting`, `if conditions`, `combination of data from multiple places` and of course setting `default` values.

__This enables you to change any input into the output you desire.__

## The Kaiba App

The kaiba App is currently in development

[app.kaiba.tech](https://app.kaiba.tech)

The app provides a user interface for creating Kaiba configurations. With the app you can map in real time easily and create the kaiba config.

## The Kaiba API

The kaiba api is open for anyone to try, you send your data and the configuration and get mapped data response.

[api.kaiba.tech/docs](https://api.kaiba.tech/docs)

## Typical usecases

* You `GET` data from api, but need to transform it for your backend system
* `POST`ing data to an api that needs data on a different format than what your system produces
* All your backends speak different language? pipe it through __Kaiba__
* Customer delivers weirdly formatted data? Use __Kaiba__ to make it sexy
* Have CSV but need nicely structured JSON? make CSV into a JSON list and transform it with __Kaiba__
* Have XML but need to change it? make it into JSON, transform it with __Kaiba__ and then dump it to XML again.
* Customers legacy system needs CSV. Use __Kaiba__ to transform your nicely structured JSON data into a JSON List that can be easily dumped to CSV

## Official Open kaiba Solutions

[kaiba-cli](https://github.com/kaiba-tech/kaiba-cli), commandline interface for file to file mapping.

[kaiba-api](https://github.com/kaiba-tech/kaiba-api), FastAPI driven rest server that maps data with kaiba

## Enterprise solutions

Coming...

## Goal

The goal of this library is to make JSON to JSON transformation/mapping easy, configurable and documentable. We achieve this by using a simple but feature-rich JSON configuration which then also acts as documentation and as a contract between parties.

## Why

Kaiba was born because we really dislike mapping. Documenting whatever decisions made in your code so that some product owner understands it is also _no me gusto_. Transforming data from one format to another is something software engineers do allmost daily... It should be easy! And documenting it shouldn't be something you have to worry about.

After the Worst POC in History we never wanted to do mapping by scripts and code again. This lead to the idea that it should be possible to create a file which governs how the structure should look and how the data should be transformed. This would then be the `single source of truth` and with Kaiba we have achieved this.

We believe that this will make collaboration between teams faster and easier. Use Kaiba to agree with data formats between Front-end and Back-end. Between the 3rd party system and your back-end. You can even use Kaiba for testing existing integrations ;-)

## Features

* Mapping with configuration File.
* [JSON Schema](https://json-schema.org/) validation of the config file.
* Structurally Transform JSON
* Combine multiple values to one.
* Default values
* If statements
    * is, contains, in, not
* Casting
    * integer, decimal, iso date
* Regular Expressions

## Contributing
Please see [contribute](https://kaiba.readthedocs.io/en/stable/contributing)

## Installation

Package is on pypi. Use pip or poetry to install

```sh
pip install kaiba
```
```sh
poetry add kaiba
```

## Introduction

Have a look at our introduction course [here](https://kaiba.readthedocs.io/en/stable/introduction)

## Quickstart
```python
import simplejson

from kaiba.process import process

my_config = {
    'name': 'schema',
    'array': False,
    'objects': [
        {
            'name': 'invoices',
            'array': True,
            'iterators': [
                {
                    'alias': 'invoice',
                    'path': ['root', 'invoices'],
                },
            ],
            'attributes': [
                {
                    'name': 'amount',
                    'data_fetchers': [
                        {
                            'path': ['invoice', 'amount'],
                        },
                    ],
                    'casting': {
                        'to': 'decimal',
                        'original_format': 'integer_containing_decimals',
                    },
                    'default': 0,
                },
                {
                    'name': 'debtor',
                    'data_fetchers': [
                        {
                            'path': ['root', 'customer', 'first_name'],
                        },
                        {
                            'path': ['root', 'customer', 'last_name'],
                        },
                    ],
                    'separator': ' ',
                },
            ],
            'objects': [],
        },
    ],
}

example_data = {
    'root': {
        'customer': {
            'first_name': 'John',
            'last_name': 'Smith',
        },
        'invoices': [
            {
                'amount': 10050,
            },
            {
                'amount': 20050,
            },
            {
                'amount': -15005,
            },
        ],
    },
}

mapped_data = process(example_data, my_config)

with open('resultfile.json', 'w') as output_file:
    output_file.write(simplejson.dumps(mapped_data))

```

contents of resultfile.json
```json
{
    "invoices": [
        {
            "amount": 100.5,
            "debtor": "John Smith"
        },
        {
            "amount": 200.5,
            "debtor": "John Smith"
        },
        {
            "amount": -150.05,
            "debtor": "John Smith"
        }
    ]
}
```
