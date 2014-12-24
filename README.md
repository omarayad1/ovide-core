# Ovide Core

[![Build Status](https://magnum.travis-ci.com/omarayad1/ovide-core.svg?token=8Fpim8KSTcqEV6F4gkPX)](https://magnum.travis-ci.com/omarayad1/ovide-core)

Core module of the ovide simulator, it contains shared modules among other Ovide applications

The main worker is currently running on ![A Heroku Dyno](http://ovide-core.herokuapp.com)

# Building & Running

## Dependencies
Python 2.7 and RabbitMQ are needed to run the application.
Install Pika:
```
pip install pika
```

A shell script is used to retrieve and build the needed dependencies:
```
chmod +x build-deps.sh
./build-deps.sh
```

## Running
Server can be started by running:
```
python worker.py
```

If, at any time, you need to clear the tasks queued for processing:
``` 
python clear_queue.py
```


## Running Tests
To run the tests, make sure you have nose installed:
```
pip install nose
```
Then run:
```
nosetests
```

# Module Structure

```
modules
|
├───compile_verilog 
│		├───compile_to_vvp(filename, filename_test)
│	 
│
├───generate_testbench
│		├───generate_testbench(filename)
│
│
├───lint_verilog
│		├───check_for_errors(filename)
│
│
├───vcdparser
│		├───parse_vcd(file, only_sigs=0, use_stdout=0, siglist=[], opt_timescale='')
│
│
├───vvp_utils
│		├───get_output(filename)
│		│
│		├───get_wave(filename)

```


# Adding Features
To add more features to the Ovide Core, simply write the Python module for the required feature as its respective function and place it in the modules folder. Then, add the new Python module in the __init__.py file in modules/.

However, don't forget to edit the routing in the API server to reference this new module.
Also, if possible add a Python Unit Test in the tests folder for the newly added feature.

# License
See LICENSE

# Roadmap
- Improve automatically generated testbench
- Move from FTP to a more suitable storage solution
- For other suggested features see Ovide-web repo
