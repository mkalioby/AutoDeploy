# Introduction

This is document shows the options avaliable in the YAML Config File.

The full file should be as follows:

### Sample File

```yaml
files:
  - source: /
    destination: /var/www/autodeploy/
  - source: test.err
    destination: /tmp
permissions:
  - object: /var/www/autodeploy/
    owner: www-data
    group: www-data
    mode: 755
    type: directory
events:
  beforeInstall:
    - location: /home/mohamed/autoDeploy/autoDeploy/exampleConfig/EventsHandler/delDir.sh
      run-as: www-data
      interpreter: bash
    - location: /home/mohamed/autoDeploy/autoDeploy/exampleConfig/EventsHandler/stopApache.sh
      run-as: root
      interpreter: bash
  afterInstall:
    - location: /home/mohamed/autoDeploy/autoDeploy/exampleConfig/EventsHandler/startApache.sh
      interpreter: bash
```

# Format

the format has three main levels:
  
## files
        these are the files that will be copied to the deployment directory. 
It should be in the format
```yaml
  - source: /
    destination: /var/www/autodeploy/
  - source: test.err
    destination: /tmp
``` 
***The format can be repeated as many as needed. Both source and destination are required.***

 The souce can be 
        
  + **File** : This is file will be copied to the destination
  + **Directory**: All the directory content will be copied to the destination. 
  
***Notes*** 
  + It should end '/' to be detected as a directory in the system.
  + Path should be relative to the working directory.
  
The destination is the folder where the file should be copied to, the system will always create the directory if it doesn't exist.

## permissions

If the special set of permission is required after the files are copied, it can be managed here.

It should be in the following format:
```yaml
permissions:
  - object: /var/www/autodeploy/
    owner: www-data
    group: www-data
    mode: 755
    type: directory
```

+ **object**: is the name of directory or file to manage (required).
+ **owner**: the name of the new owner of object (optional)
+ **group**: the name of the new group which owns the object (required if owner is there)
+ **mode**: the permission previliages as integers (optional)
+ **type**: the type of the object, if it is a directory, the rule will be applied on all the children files and directories.

## events
events are an optional part where you can tell the deployer to run special scripts before or after the deployment.

Currently, there are 2 events to handle.

+ **beforeInstall**: Which be called before anything is done, usually this is used to stop any working servers
+ **afterInstall**: which is called after the everything is done, usually this is used to start the server back.

It should be in the following format:

```yaml
beforeInstall:
  - location: EventsHandler/delDir.sh
    run-as: www-data
    interpreter: bash
```

+ **location**: the relative path of the script to run.
+  **run-as**: the username of the user who will run this command (optional).
+  **interpreter**: the name of the interpreter that should be used to run the script (optional but highly recommended)
  
