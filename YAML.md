# Introduction

This is document shows the options avaliable in the YAML Config File.

The full file should be as follows:

```yaml
files:
  - source: index.html
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
        these are the 
