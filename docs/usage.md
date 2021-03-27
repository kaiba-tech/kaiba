The goal of this library is to make configurable data transformation(mapping) easy and flexible.

We have decided to only support json to json mapping. This is because quite frankly its impossible to have configurable mapping that works on any format. We chose json because its quite easy to make anything into json and its quite easy to make json into anything.


## Running Kaiba

There are multiple ways of running Kaiba with the most convenient for testing being with `kaiba-cli`. Then theres `kaiba-web` which is a webserver where you can post configuration and data, and it returns the mapped result. Last but not least, theres running `kaiba` as a package in your python code. This section will shed light on when to use which and add some quickstart examples.

### Kaiba CLI

The Kaiba CLI is the easiest way to get started. All you need is python>=3.6 on your system. You also do not need to write any python code.

usefull when:

* Testing if Kaiba could be interesting for you
* Need to trigger mapping with scheduling tools like Cron or Windows Service
* You are using a different programming language, but can execute cmd scripts

the [introduction](../introduction) uses kaiba-cli, head over there for a quick start

### Kaiba WEB

Kaiba Web is a web api built with the [falcon framework](https://falconframework.org/). We have one-click deploy buttons for `GCP Run` and `Heroku`. It enables you to very easily set up a webserver where you can post configuration and raw data in the body and get mapped data in the body of the response. This also does not require to write any python code.

Usefull when:

* You can loadbalance it and deploy multiple instances
* You are on a platform like GCP, AWS, Heroku
* You are already in a microservice/webservice oriented environment

Look at the [git repo](https://github.com/greenbird/kaiba-web) for deployment guide

### Kaiba python package

If you already are using Python and just want to add Kaiba, you can easily import it into your program and run the code. This makes the most sense when you need to handle the data before or after the Kaiba transformation for example when you need to dump result to xml.

Usefull when:

* You need to do extensive handling of input data before mapping
* You need to transform the output json into something else

Caveats:
Remember that the more you handle the data before or after Kaiba, the more you must document your changes to the data.

To use Kaiba, import the process function and feed it your data and the configuration.

```python
from kaiba.process import process

your_data = []
your_config = {}

result = process(your_data, your_config)
```

Notice that process expects `data: Union[List, Dict]` and `configuration: Dict`
