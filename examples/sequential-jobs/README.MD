# Sequential Job Tutorial

# TODO list
1. [important] How to get logs if pod is error
2. Furnish the job template
3. test if the template works.

## FAQ


### supported format
```yaml
# Command to run


# Choice 1
args:
- sh
- path_to_your.sh 

# Choice 2

args:
- sh
- "sh command"

# Choice 3
args:
- python
- script.py
- aa=bb
- cc=dd 
# ...
```

### log is not working properly.

If you cannot see python `print` in this command, `kubectl logs`, try setting `PYTHONUNBUFFERED=0`