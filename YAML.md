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

the file has three main levels:
  
## files
        these are the files that will be copied to the deployment directory. 
It should be in the format
```yaml
  - source: /
    destination: /var/www/autodeploy/
  - source: test.err
    destination: /tmp
``` 
 The souce can be 
        
  + **File** : This is file will be copied to the destination
  + **Directory**: All the directory content will be copied to the destination. 
  
  ***Notes*** 
    + It should end '/' to be detected as a directory in the system.
    + Path should be relative to the workig directory.
  
  
        


        
        
