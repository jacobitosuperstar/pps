# Production and Planning Software

- [SET UP](#set-up)
  - [RUNNING THE APP](#running-the-app)
  - [STOPPING THE APP](#stopping-the-app)
- [BACKEND](#backend)
  - [RUNNING THE TESTS](#running-the-tests)
  - [EMPLOYEE](#employee)
    - [CREATE EMPLOYEE](#create-employee)
    - [MODIFY EMPLOYEE](#modify-employee)
    - [DELETE EMPLOYEE](#delete-employee)

# SET UP
## RUNNING THE APP

To user the application having docker installed in your computer is a must, and
you can download it from this [link][1]

to run the application locally, from the command line you can run the command
`docker-compose up` from the `pps` directory. To run the application as a
background or detached from the terminal window, you can run the command
`docker-compose up -d` or `docker-compose up --detach`.

To run commands inside the `web` service container you can run this while the
application is running.

`docker-compose exec web /bin/bash`

With this you will be able to be in the server environment and run magene
commands if needed.

## STOPPING THE APP

To stop the application you can use `docker-compose down` from the terminal in
the `PointBluePython` directory.

If you want to completelly stop the application, remove the images and the
volumes, you can use the following command:

`docker-compose down --rmi 'all' -v`

Breaking down the command

- `docker-compose down`: This is the standard command to stop and remove
containers, networks, and volumes associated with a Docker Compose application.

- `--rmi 'all'`: This option tells Docker Compose to remove all images
associated with the services defined in your docker-compose.yml file. The all
argument specifies that you want to remove all images, not just the ones that
are no longer in use. This can be useful to clean up images that are no longer
needed.

- `-v`: This option tells Docker Compose to also remove volumes. Volumes are
used to persist data between container restarts. When you include this option,
Docker Compose will remove not only containers and networks but also the
volumes associated with your services. Be cautious when using this option, as
it can result in data loss if not used carefully.

# BACKEND

## RUNNING THE TESTS

To run the tests, you have to enter to the bash environment in the `web`
service, and now in that bash environment, check that you are in the correct
folder, and run `python manage.py test` to execute all the tests, or if you
want to run the tests of a single module you can run
`python manage.py test {module_name}`

## EMPLOYEE

[1]: https://www.docker.com
