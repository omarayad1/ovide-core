# Ovide Core

[![Build Status](https://magnum.travis-ci.com/omarayad1/ovide-core.svg?token=8Fpim8KSTcqEV6F4gkPX)](https://magnum.travis-ci.com/omarayad1/ovide-core)

Core module of the ovide simulator, it contains shared modules among other Ovide applications

## Dependencies
Python 2.7 and RabbitMQ are needed to run the application. 

## Building & Running
A shell script is used to retrieve and build the needed dependencies:
```
chmod +x build-deps.sh
./build-deps.sh
```

Server can be started by running:
```
python worker.py
```

If, at any time, you need to clear the tasks queued for processing:
``` 
python clear_queue.py
```


## Running Tests


## Adding Features
To add more features to the Ovide Core, simply write the Python module for the required feature as its respective function and place it in the modules folder.
However, don't forget to edit the routing in the API server to reference this new module.

## License
See LICENSE
