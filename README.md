# Repository template for developing with python

This template can be used to jumpstart and unify development in python. It was generated
using
the [pyopensci python package template](https://github.com/pyOpenSci/pyos-package-template)
and [copier](https://github.com/copier-org/copier):

```bash
copier copy gh:pyopensci/pyos-package-template
```

The resulting project was filled with a simple example application and extended with
dockerization.

- [Quickstart](#quickstart)
- [Project structure](#project-structure)
- [Logging](#logging)
- [Configuration](#configuration)
- [CI/CD pipeline](#cicd-pipeline)
- [Copyright](#copyright)

This application is also used to demonstrate how to create a FLECS app
here: [https://github.com/FLECS-Technologies/apps-tech.flecs.template-py](https://github.com/FLECS-Technologies/apps-tech.flecs.template-py)

## Quickstart

1. Create a new repository by clicking on the `Use this template` button on the top
   right
   or [here](https://github.com/new?owner=Somic-Flecs-shared-space&template_name=development-template-rs&template_owner=Somic-Flecs-shared-space)
2. Clone your new repository
3. Adjust project meta information in [pyproject.toml](./pyproject.toml) e.g.
    1. Project name
    2. License
    3. Authors
4. Rename the module `dev_template_py` as you wish
5. Set up [Variables and secrets](#variables-and-secrets)
6. Commit all changes

## Project structure

You can read more about the project structure in [DEVELOPMENT](./DEVELOPMENT.md).

## Logging

This project uses [logging](https://docs.python.org/3.13/library/logging.html)
in combination with a config file that controls logging format and filters.
See [Configuration](#configuration) for more information about the configuration file.

## Configuration

The template project uses a `log_conf.yaml` file for configuration. It is expected to be
passed as an argument to `uvicorn` on startup. As done in
the [Dockerfile](./docker/Dockerfile) or the dev script
of [pyproject.toml](./pyproject.toml). Look at
the [python documentation](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)
for the format of the file. The config that is used for the built image is located
at [./docker/fs/config/log_conf.yaml](./docker/fs/config/log_conf.yaml).

## CI/CD pipeline

### Variables and secrets

The CI/CD pipeline expects certain variables and secrets to build and deploy your
application. If you only want to use
the GitHub container registry for your container images, you do not need any secrets and
just the `APP_NAME` variable,
but need to look
at [Deploy to GitHub container registry](#deploy-to-github-container-registry).

#### Secrets

`DOCKER_REGISTRY_USER` and `DOCKER_REGISTRY_PASSWORD` define the username and password
needed to authenticate with your
container registry.

Take a look at
the [GitHub Docs](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/using-secrets-in-github-actions)
for more information.

#### Variables

`DOCKER_REGISTRY` defines the container registry the images will be uploaded to.
`DOCKER_REGISTRY_NAMESPACE` defines the namespace the images will be uploaded to, e.g.
`apps`. You only have to define this variable if you want to deploy to a namespace.
`APP_NAME` defines the name of you application, it will be used for the image name.

Take a look at
the [GitHub Docs](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables)
for more information.

### Deploy to GitHub container registry

If you want to deploy to the GitHub container registry you have to make some
adjustments:

- Remove the if condition in [release_ghcr.yml](.github/workflows/release_ghcr.yml)
- Set a correct value for the inputs `app_name` and `registry_namespace`
  in [release_ghcr.yml](.github/workflows/release_ghcr.yml) for the jobs `build_image`
  and `deploy_ghcr`
- Remove the if condition in the `docker_ghrc` job
  in [pull_request_validate.yml](.github/workflows/pull_request_validate.yml)
- Set a correct value for inputs `app_name` and `registry_namespace` in the
  `docker_ghrc` job
  in [pull_request_validate.yml](.github/workflows/pull_request_validate.yml)
- If you do not want to use another container registry
  delete [release.yml](.github/workflows/release_ghcr.yml) and the
  job `docker`
  in [pull_request_validate.yml](.github/workflows/pull_request_validate.yml)

### Workflows

#### Validate pull requests

The workflow defined
in [pull_request_validate.yml](.github/workflows/pull_request_validate.yml) will run
automatically
on every pull request but can be manually triggered as well.

##### lint

Lints the projects code and documentation.

##### test

Tests the installation and types. The automatic tests (e.g. unit tests) are executed.

##### build

The project is built and the resulting .whl files are uploaded as artifacts.

##### Determine tag

Determines the tag of the docker image that will be used from now on. If the workflow is
called from a PR the tag will
be `pr-{pr-number}` otherwise it will contain the short form commit hash and look like
`commit-{commit-sha}`.

##### Docker

Creates docker images. See [Build image](#build-image) for more details.

#### Build image

The workflow defined in [build_image.yml](.github/workflows/build_image.yml) builds
docker images for the three
supported architectures and attaches them as artifacts. Look at the description of the
inputs for more information.

#### Deploy image

The workflow defined in [deploy_image.yml](.github/workflows/deploy_image.yml) deploys
the previously built docker
images to the GitHub registry. Look at the description of the inputs for more
information.

#### Release

The workflow defined in [release.yml](.github/workflows/release.yml) is executed on
published releases. It builds
docker images and deploys them to the container registry defined
via [Variables and secrets](#variables-and-secrets). The tag for the images corresponds
to the git tag of the release.
See [Build image](#build-image) and [Deploy image](#deploy-image) for more details.
The workflow defined in [release_ghcr.yml](.github/workflows/release_ghcr.yml) does the
same but for the GitHub
container registry.
See [Deploy to GitHub container registry](#deploy-to-github-container-registry) for more
information.

## Copyright

- Copyright © 2025 FLECS Technologies GmbH.
- Free software distributed under the [MIT License](./LICENSE).
