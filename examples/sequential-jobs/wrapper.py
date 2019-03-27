"""
This is the wrapper to read and get the scripts to be sequential runnable.

"""
import os

import yaml
import copy
import argparse

KILL_BUFFER_TIME = 180  # 3 minute to force kill

parser = argparse.ArgumentParser('Hello world')

parser.add_argument('--f_path', type=str, required=True,
                    help="This is the file path to your .yaml.")
parser.add_argument('--runtime', type=float, required=False, default=3.0,
                    help="This is time each run lasts. Default is 3 hours.")
parser.add_argument('--uid', type=int, required=False, default=-1)
parser.add_argument('--username', type=str, required=False, default='')
parser.add_argument('--run_interval', type=float, required=False, default=3.0,
                    help='deprecated.')
parser.add_argument('--num_runs', type=int, required=False, default=1,
                    help='Number of runs ')

def merge_list_str(l_str):
    a = ''
    for i in l_str:
        a += i + ' '

    return a


def read_yaml_file(f_path):
    with open(f_path, 'r') as f:
        config = yaml.load(f)
    return config


def handle_args(args):
    if args.runtime > 3.0:
        print("Change running time to 3.0 hour.")
        args.runtime = 3.0
    if args.num_runs < 1:
        raise ValueError("Num runs must be >= 1.")
    return args


def obtain_job_template():
    return read_yaml_file('job_template.yaml')


def process_yaml_pod(config, args):
    specs = config['spec']
    metadata = config['metadata']

    # Parse UID into security Context if necessary.
    if 'securityContext' in specs.keys():
        if args.uid > 0:
            specs['securityContext']['runAsUser'] = args.uid

    if 'user' in metadata['labels'].keys():
        metadata['labels']['runUser'] = args.username if args.username != '' else metadata['labels']['user']
    else:
        metadata['labels']['user'] = args.username
        metadata['labels']['runUser'] = args.username

    if len(specs['containers']) > 1:
        Warning("The containers in your kubernetes file should not be more than one! Use only the first one. ")

    new_container = copy.deepcopy(specs['containers'][0])
    if 'sleep' in new_container['command'] and 'infinity' in new_container['command']:
        raise ValueError("You shall not submit sleep infinity pod here. "
                         "Please run your script or, e.g., python train.py instead")

    if 'args' in new_container.keys():
        combine_cmds = new_container['command'] + new_container['args']
    else:
        combine_cmds = new_container['command']

    new_container['command'] = ['/bin/bash', '-c']
    cmd_tmout = f'timeout -k {KILL_BUFFER_TIME} {args.runtime}h '

    # new_container['command'] = ['timeout', '-k', str(KILL_BUFFER_TIME),
    #                             str(args.runtime) + 'h']
    assert combine_cmds[0] in ['python', 'sh'], "Your args should begin with 'sh' or 'python' "
    cmd_to_run = merge_list_str(combine_cmds)
    new_container['args'] = [cmd_tmout + cmd_to_run +
                             '; if [ $? -eq 124 ] || [ $? -eq 137 ]; '
                             'then exit 0; '
                             'else exit $?; '
                             'fi']
    num_runs = args.num_runs

    # overwrite job template accordingly.
    job_config = obtain_job_template()

    # assign the metadata
    job_config['metadata'] = metadata
    job_template = job_config['spec']['template']
    job_template['metadata']['name'] = new_container['name']
    j_spec = job_template['spec']

    # substitute the job containers with the template one.
    job_container = j_spec['containers']
    j_spec = specs
    j_spec['containers'] = job_container

    # Replace the initContainers with the original containers.
    j_spec['initContainers'] = []
    j_init = j_spec['initContainers']
    for i in range(1, num_runs+1):
        j_cont = copy.deepcopy(new_container)
        j_cont['name'] = f'job-{i}'
        j_init.append(j_cont)

    # overwrite it again.
    job_config['spec']['template']['spec'] = j_spec
    # Add the listener pod.
    return job_config


def process_yaml_job(config, args):
    raise NotImplementedError("To support later.")


if __name__ == '__main__':
    args = parser.parse_args()
    args = handle_args(args)

    f_path = args.f_path
    config = read_yaml_file(f_path)
    if config['kind'] == 'Pod':
        new_config = process_yaml_pod(config, args)
    elif config['kind'] == 'Job':
        new_config = process_yaml_job(config, args)
    else:
        raise NotImplementedError("Only support kind: Pod or Jobs, got {}".format(config['kind']))

    dirname = os.path.dirname(f_path)
    basename = os.path.basename(f_path)

    print(new_config)
    w_path = os.path.join(f_path + '.job')
    with open(w_path, 'w') as f:
        print("Dumping the new config to " + w_path)
        yaml.dump(new_config, f, default_flow_style=False)

