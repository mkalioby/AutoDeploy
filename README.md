# AutoDeploy
Building an automated deployment system which is similar to AWS CodeDeploy but is hostable inside enterprise.

The target is to minimize the manual prone errors of code deployment.

The project has the following componemts:
* **Deployment Daemon** (to run under root role so it can restart servers).
* **Deployment Client** (which can communicate with the server giving it the scripts to run).
* **Deployment Interface** (to see the progress and it can be used to deploy certain code versions).

The deployment configuration will be based on YAML Format. The full specification can be [here.](https://github.com/mkalioby/AutoDeploy/blob/master/YAML.md)

The client should be callable from CI systems (like Jenkins) to deploy the code after a successful build.

##Events:##

The following events will be handled by the system:

1. **beforeInstall**: This event will run after the code is downloaded, normal will be used to stop servers/decrypt files
2. **Install**: doing the deployment operation itself
3. **afterInstall**: Actions required after Installing like reloading a server.
4. **Validation**: An optiomal step to make sure that everything is OK.

Every event should have the following format:

```yaml
events:
   event-name
       - location: script-location
         runas: user-name
  ```
## Requirments ##
### For the Server:
* pyyaml (>3.0)
* pycrypto

### For the web-application
* django 1.8.1+
* django-table-2
* django-table-report

## Installation ##

An Installation guide is avaliable [here.](https://github.com/mkalioby/AutoDeploy/blob/master/Installation.md)
