# Thorgate's Django template (Bootstrap 4 variant)

[![Build status](https://gitlab.com/thorgate-public/django-project-template/badges/master/pipeline.svg)](https://gitlab.com/thorgate-public/django-project-template/commits/master)

[Django](https://www.djangoproject.com/) project template that we use at [Thorgate](https://thorgate.eu).

Best suited for medium-sized and bigger apps that use JavaScript and React for frontend.

See also the [Single-Page Application](https://gitlab.com/thorgate-public/django-project-template/tree/spa)
and [Bootstrap 3](https://gitlab.com/thorgate-public/django-project-template/tree/legacy-docker-bootstrap3) variants.

_(note that the primary repo is in [Gitlab](https://gitlab.com/thorgate-public/django-project-template), with mirror in [Github](https://github.com/thorgate/django-project-template))_


## Features

- Django-based backend

    - [Django](https://www.djangoproject.com/)
    - Separate settings for different environments (local/staging/production)
    - Python 3.6 or later

- Frontend app(webapp) with JavaScript (ES2015), React and Sass

    - Latest JavaScript features from [ES2015](https://babeljs.io/docs/learn-es2015/) and beyond, transpiled with
      [Babel](https://babeljs.io/)
    - [React](https://facebook.github.io/react/) 16 for fast modular user interfaces
    - [Sass](http://sass-lang.com/), [PostCSS](http://postcss.org/) and
      [Autoprefixer](https://github.com/postcss/autoprefixer) for more convenient styling
    - [Webpack](https://webpack.github.io/) 2.3 is used to bundle and minify JavaScript and styles

- Batteries

    - Docker / Docker Compose integration
    - Linting of Python, JavaScript and Sass code with [Prospector](http://prospector.landscape.io/),
      [ESLint](http://eslint.org/) and [stylelint](https://stylelint.io/)
    - [py.test](http://pytest.org/) and [coverage](https://coverage.readthedocs.io/) integration
    - Deploy helpers, using [Fabric](http://www.fabfile.org/)
    - Media files are stored in a CDN like S3 or Google Cloud Storage
    - Out-of-the-box configuration for nginx, gunicorn and logrotate
    - Includes [PyCharm](https://www.jetbrains.com/pycharm/) project config


## Usage

To use this template, first ensure that you have
[Pipenv](https://pipenv.readthedocs.io/en/latest/) `2020.6.2` available.

After that, you should:

1. Install the requirements of the project template by running
    ```
    pipenv install
    ```
2. Activate the virtualenv created by pipenv:
    ```
    pipenv shell
    ```
3. Navigate to the directory where you'd like to create your project:
    ```
    cd /home/my-awesome-projects/
    ```

4. Create a new project by executing:
    ```
    cookiecutter dir/to/django-project-template/
    ```


It will ask you a few questions, e.g. project's name.

After generation completes, **you should deactivate virtual environment for cookiecutter**,
search for any TODOs in the code and make appropriate changes where needed.

See README.md in the generated project for instructions on how to set up your development environment.


## Upgrading project template

First ensure you have a python3 interpreter with `cookiecutter` installed.

To upgrade an existing project, change the current working directory to the root of the project you want to upgrade. i.e. `cd project-to-upgrade`. Ensure your are not in the `template` branch.

Then run `python ~/path/to/django-project-template/upgrade-template.py`

This will make a commit to the branch `template` in your project with the updates to the project template. Then merge the `template` branch.

## Docker images

The template uses our own images for CI runs. One for the template itself and a second one
for generated projects. Both images are alpine based and contain python3, pip and some support
packages. The images are published to [repository container registry](https://gitlab.com/thorgate-public/django-project-template/container_registry) and also to [docker hub](https://hub.docker.com/u/thorgate).

The images are built in CI (from default branches only) and also updated every day via schedules.

**Project CI Image**

- [Dockerfile-ci](./utils/Dockerfile-ci)
- Image in repository registry: `registry.gitlab.com/thorgate-public/django-project-template/ci`
- Image in docker hub: `thorgate/django-template/ci`
  - [see online](https://hub.docker.com/r/thorgate/django-template/ci)

**Template CI Image:**

- [Dockerfile-base-ci](./utils/Dockerfile-base-ci)
- Image in repository registry: `registry.gitlab.com/thorgate-public/django-project-template/base-ci`
- Image in docker hub: `thorgate/django-template/base-ci`
  - [see online](https://hub.docker.com/r/thorgate/django-template/base-ci)
