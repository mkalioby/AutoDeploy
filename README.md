# autoDeploy
Trying to build an automated deployment system which is similar to AWS CodeDeploy.

The target is to minimize the manual prone errors of code deployment.

The project will have the following componemts:
* **Deployment Daemon** (to run under root role so it can restart servers).
* **Deployment Client** (which can communicate with the server giving it the scripts to run).
* **Deployment Interface** (to see the progress and it can be used to deploy certain code versions).

The deployment job will be based on YAML Format, the multiple values can be seprated by ','.

The client should be callable from CI systems (like Jenkins) to deploy the code after a successful build.

##Events:##

The following events will be handled by the system:

1. **Before Install**: This event will run after the code is downloaded, normal will be used to stop servers/decrypt files
2. **Install**: doing the deployment operation itself
3. **After Install**: Actions required after Installing like reloading a server.
4. **Validation**: An optiomal step to make sure that everything is OK.

Every event should have the following format:

```yaml
events:
   event-name
       location: script-location (can be seprated by ',')
       runas: user-name
  ```
## Requiremnts ##
* pyyaml (>3.0)
