""" A set of functions to interact with code execution in an isolated docker
sandbox."""
from docker import Client
import os
import tempfile

# create mapping for languages
lang_config ={
   "python2":{
      "command":"python /mnt/data/input.py",
      "image":"python2",
      "ext":"py"
   },
   "python3":{
      "command":"python /mnt/data/input.py",
      "image":"python3",
      "ext":"py"
   },
   "nodejs":{
      "command":"node /mnt/data/input.js",
      "image":"nodejs",
      "ext" : "js"
   }
}

def query_images():
    """ Return a list of images that are used by this machine to execute
    aribitary code. We return the language names. """
    cli = Client(base_url='unix://var/run/docker.sock', version='auto')
    images = cli.images()

    # only interested in the tag names
    tags = [image['RepoTags'][0] for image in images]
    tags = [tag for tag in tags if tag.startswith('quicktry-')]

    return tags


def execute(workdir, data, stdin, language):
    # create the client to the docker service
    cli = Client(base_url='unix://var/run/docker.sock', version='auto')

    options = lang_config.get(language)
    if not options:
        print("{} does not exist".format(language))
        return ""

    # generate the temporary path for the worker
    with tempfile.TemporaryDirectory(dir=workdir) as dirpath:
        # create the input file
        input_file="input.{}".format(options["ext"])
        with open(os.path.join(dirpath, input_file), 'w') as f:
            f.write(data.encode().decode('unicode_escape'))

        # define the docker container. mount a temporary directory for the
        # input file
        host_config = cli.create_host_config(
                binds=['{}/:/mnt/data'.format(dirpath)])

        # TODO: handle stdin
        container = cli.create_container(
                volumes = ['/mnt/data'],
                host_config = host_config,
                image = "quicktry-{}:latest".format(options['image']),
                command = options['command'])

        # run the script and read stdout
        # TODO: error handling
        c_id = container.get('Id')
        cli.start(container=c_id)
        cli.wait(container=c_id)

        output = cli.logs(container=c_id, stdout=True)

        return output
