# autoDeploy
Trying to build an automated deployment system which is similar to AWS CodeDeploy.

The target is to minimize the manual prone errors of code deployment.

The project will have the following componemts:
* Deployment Daemon (to run admin role so it can restart servers).
* Deployment Client (which can communicate with the server giving it the scripts to run).
* Deployment Interface (to see the progress and it can be used to deploy certain code versions).

The deployment job will be based on YAML Format, the multiple values can be seprated by '',.
