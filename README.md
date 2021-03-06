# QuickTry

QuickTry is a flask service and library for sandboxing arbitrary script execution using
docker.

This application was developed for OSHacks @ Github HQ to quickly read,
execute, and print code snippets from stackoverflow. This project contains
scripts to manage sourced docker images, a library to remotely execute
arbitrary code safely, and a web application to service endpoint.

## Getting started
This project depends on docker and python3, and use of virtualenv is
encouraged. This setup was tested on Mac OSX and Ubuntu 14.04.

### Installation
1. Create and activate the project environment.
```
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

2. Update the list of docker images. This should be run if this is your first
time or if there have been changes to the list of supported languages.
```
$ ./rebuild_docker.sh
```

3. Run the validation script. This lets you know that everything is working
reasonably well.
```
$ python test.py
```

### Running the service
We can run the service locally using the following convenience script.
```
$ ./run.sh
```
Note that if you are running on linux, you may need administrative access to
access the docker socket in the sandbox. Verify that the script is
acceptable to run as root, and prefix the above command with `sudo`.

Alternatively, if you prefer to run things by hand, make sure that the
FLASK_APP variable is set to the top level app.py and a temporary work
directory is declared (currently hardcoded to be tmp in app.py).
```
$ mkdir tmp                 # this may go away
$ export PYTHONPATH=`pwd`   # flask cli needs the relative path to quicktry
$ export FLASK_APP=quicktry
$ flask run
```

You will now be able to access the locally hosted service by browsing to
`localhost:5000`. Try creating a request to verify that everything is working.

Using cURL:
```
$ curl -H "Content-Type: application/json" \
       -X POST -d '{"lang": "python2", "code":"print(\"hello world\")"}' \
       localhost:5000/run
```

Using httpie:
```
$ http GET localhost:5000/run code="print('hello')" lang="python2"
```

## Deployment
Testing this project locally is straightforward. Use with caution whenever
exposing your service to the world wide web, docker isn't the be all end all
for task isolation.

### Localhost deployment
Follow the `getting started` portion of the README. This should give you an
instance that is accessible to `localhost:5000`.

### Localhost tunnelling with ngrok
To determine that this application suits your needs, you can
reproduce a publicly accessible instance quickly using ngrok to tunnel
localhost traffic to a public endpoint.

First set up ngrok by following the [getting started
documentation](https://dashboard.ngrok.com/get-started). Once you have
installed your authentication token, run the following command to tunnel all
traffic against localhost:5000 to a public endpoint.

```
$ ./ngrok http 5000
```

Port 5000 is the default port for flask development; adjust the value for your
specific use case.

### uWSGI and Nginx
Refer to the README in the `production/` folder. This provides a systemd Unit
 file, uWSGI configuration, and an Nginx block configuration that can be
 copied to their proper locations.

## Contributing
Contributions and suggestions are welcomed and encouraged.

### Adding support for a new language
Adding a new language to this service is straightforward.

1. Find a dockerfile that supports the new language
    * Add this file under `/docker-images/<language-name>/Dockerfile`
2. Update the `docker images`
    * run `./rebuild_docker.sh`
3. Register the new language with quicktry
    * Add a new entry to `languages.yml` with the following information:
        - language name
        - command to run
        - the file extension

Add a new validation test under `test.py` to make sure that the new language
works as expected.

### Wishlist
QuickTry works for the simple use-case, but could be a more robust platform for
sandboxed code execution. These are a few things that could be done better.

* Remove all TODOs
* Automated testing and unit tests
* Verify sandboxing properties of docker in-depth
* Throttling and rate-limiting of requests to prevent service outages
* Creating a capped worker pool and request queue
* Decoupling the management of docker workers from flask service
* Deployment to a production server

## Credits
Kudos to the whole QuickTry team at OS Hacks for creating something that just
works. :thumbsup:

### Related works
Here are some other projects that were researched as viable canidates for
QuickTry, but were passed on in favor of a do-it-ourselves solution.

* [remoteinterview/compilebox](https://github.com/remoteinterview/compilebox).
* [edx/codejail](https://github.com/edx/codejail)

### Dockerfile sources
The docker images have been sourced from a variety of places, so we have
aggregated them here so you can view them from the source.

* [jfloff/alpine-python](https://github.com/jfloff/alpine-python)
* [frol/docker-alpine-python3](https://github.com/frol/docker-alpine-python3)
* [nodejs/docker-node/6.3](https://github.com/nodejs/docker-node)
* [frol/docker-alpine-go](https://github.com/frol/docker-alpine-go)

## License
QuickTry is released under the MIT License.

