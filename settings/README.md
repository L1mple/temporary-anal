# Settings

Folder that contains settings for different environments for application.
Specifically it provides settings for debug environment and docker environment.

**Debug environment** is required for local run of application for debugging
purposes.

**Docker environment** is required for locally deployed service dependencies and
service itself if one is deployed in Docker for different kind of testing and
debugging purposes.

No actual configuration options can be present in this file. If you have some
separated dev stands then consider placing settings apart from repository
(gitignore them for example).

This files are for local development only.

`debug.env` is already used in launch json configuration and passed to `FastAPI
| Debug` launch configuration.

`docker.env` is already used in `Docker Compose Up | Debug` VS Code task.
