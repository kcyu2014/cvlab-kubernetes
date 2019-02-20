# CVLab Kubernetes Tutorials
EPFL CVLab Kubernetes (k8s) tutorials with true training examples 🤩
Ideally, with this tutorial, you should smoothly transit your code on cvlab-servers to k8s 
without any problem! Let's see what's the steps are.

If you are interested to read how k8s works, please read this.
> Thanks to Zheng for pointing to this wonderful blog. 
[Kubernetes 101: Basic ideas.](https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16)
 
### Table of contents:
* [Prerequisites](##Prerequisite)
* [Introduction to docker and build your own image](##Docker-image)
* [How to design your k8s yaml config](##Kubernetes)
* [Example project: Step-by-step transition to k8s](##Example-Project) 
* [Training FAQs: Please read this before deploying jobs](##Training-FAQs)

Some useful sections: 
- [Dockerfile Templates]()
- [Kubernetes Templates]()

## Prerequisite
### 1. Install kubernetes
* Install k8s on cvlab servers **without root access**.

```bash
# Downloads the latest version.
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

# Make it executable. 
chmod +x ./kubectl

# Move kubectl into your path.
mv ./kubectl <one path in your $PATH variable>
```

Please refer to [official link](https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-binary-using-curl) 
for more information.

* Install k8s on your macOS. 
```bash
brew install kubernetes-cli
kubectl version # to check if kubectl is successfully installed.
```

### 2. Copy your key file into the `$HOME/.kube`.
Before begin, make sure you have request your key-files from the admin.

```bash
mkdir ~/.kube
mv <user-name>.config ~/.kube/config  # have to change the name.
mv <user-name>.crt ~/.kube
mv <user-name>.key ~/.kube
```

You are now ready to begin k8s journey! If you install this on your local computer, 
make sure you are connected to EPFL's vpn.

## Docker image
> This section is adapted from MLO EPFL to 
help you customize docker image, for CVLabers.
Thanks to MLO EPFL group for putting a nice documentation for us.

To use a kubernetes pod, you need to:
 - [Create a Dockerfile with your needed config](#creating-a-dockerfile)
 - [Build a Docker image](#building-a-docker-image)
 - [Push the docker image to ic-registry.epfl.ch/cvlab/](#pushing-the-docker-image)
 - [Create a kubernetes config file](#creating-a-kubernetes-config-file)
 - [Dockerfile Templates](#Dockerfile-Templates)
 
 
### Creating a Dockerfile

If you are new to docker, have a look at this very simple 
[Dockerfile](). 
You should guess what is happening and add your own config.

Put your gaspar id after `NB_USER=` and your uid after `NB_UID=`.\
You can get you uid by using the `id` command on a cluster.

The `FROM` line allows you to choose an image to start from. You can choose from images on the [Dockerhub](https://hub.docker.com/) (or elsewhere).

### Building a Docker image

Once you are happy with the Dockerfile, go to the directory of the Dockerfile and run:
```bash
docker build . -t <your-tag>
```
Replace `<your-tag>` by the name you want to give to this Docker image.\
It is good practice to put your name first, for example `kyu_base`.

### Pushing the Docker image
When you will create a pod, the server will need a Docker image to build a container for you.\
The server will go look for the docker image on https://ic-registry.epfl.ch/, so you should put your Docker image there.

Go have a look at https://ic-registry.epfl.ch and use your gaspar credentials to login in.

There already is a group project named `cvlab`. 
Please ask someone in the lab already using kubernetes to add you to the cvlab group so that you can push your Docker image to that repository.

#### Login Docker to ic-registry.epfl.ch/cvlab/
Login to the server by running the following command and entering your epfl credentials:
```bash
docker login ic-registry.epfl.ch
```
This is a 'one-in-a-lifetime' steps.

#### Actually pushing the Docker image
To push an image to a private registry (and not the central Docker registry) you must tag it with the registry hostname.\
Then you can push it:
```bash
docker tag <your-tag> ic-registry.epfl.ch/cvlab/<your-tag>
docker push ic-registry.epfl.ch/cvlab/<your-tag>
```


### Dockerfile Templates
Here we provide a set of templates for most deep learning frameworks that most people use.
- [Matlab with MatConvNet]()
- [PyTorch]()
- [TensorFlow]()


## Kubernetes

### Creating a kubernetes config file
Have a look at (and download) this simple [kubernetes config file](https://github.com/epfml/kubernetes-setup/blob/master/templates/pod-simple/pod-gpu-mlodata.yaml).
Fill all elements that are in \<brackets\> .\
`<your-pod-name>` needs not be the same as `<your-docker-image-tag>` but again it is good practice to put your name first for the pod name, for example `jaggi-pod`.

In this config file,
 - you can change: `nvidia.com/gpu: 1` to request more gpus
 - you can see at the end that mlodata1 is mounted. You can remove it or change it for mloscratch
 - you specify which command is run when launching the pod. Here it will sleep for 60 seconds and then stop
 
 #### Commands

- To have a container run forever (for debugging purpose), you can use:
   ```yaml
   command: [sleep, infinity]
  ```
  and then you can [connect to the pod through ssh](#ssh-to-a-pod) and run your jobs from there.

  **If you do this, make sure to**
    - **[delete the pod](#deleting-a-pod) once you are done to free the resource !**
    - **Request only 1 GPU for the sake of other people!**

- To run more complex or multiple commands, you can do:
  ```yaml
   command: ["/bin/bash", "-c"]
   args: ["command1; command2 && command3"]
  ```
  OR directly run python command from Working DIR.
  
  For example:
  ```yaml
   command: ["/bin/bash", "-c"]
   args: ["cd /cvlabdata1/home/kyu && python automl.py"]
  ```

  _The resource will be automatically freed once the command has run. The pod gets status `Completed` but is not deleted._

[TODO]
1. Creation of pods.
- A linux pod
- With GPU
- With GPU and libraries ??

2. Run pod in a correct way
  - Do not use **sleep and infinity**
  - Try to debug locally and then deploy
  - Deploy command examples
  ```bash
  ['python', ... ]
  ```

3. introduction to kubenetes Job
 - Yaml Job config
 - Create multiple jobs with hyper-parameter changing with help of `Jinja2`.
  

## Training-FAQs

Q1. How do I use Tensorboard/Visdom/ .... to monitor my training if I cannot access it like a normal server?

> Check the examples in <WILL ADD LATER>.

Q2. How do I **debug** if I cannot use `sleep infinite`?

> Solution 1: Debug on normal server and then deploy.
 
> Solution 2: print your logs into file so that you can check debugging message there.
```yaml
command: ['/bin/bash', '-c']
args: ['python something.py -args... > logs/debug-run-1.txt']
```

Q3. How can I run with PyCharm debugger?
 
It's possible but quite dirty solution. It requires the SSH enabled pod. Ideally, k8s 
is for people to **deploy but not debugging**, so if you need to debug densely, please use 
those old servers and let k8s only for training.  

4. How do I stop other people eating all the resources?

> Victor: Wall of shame. If three strike on the WoS, no GPU for 2 weeks.

> Kaicheng: Please buy us beers to avoid us killing those crazy pods.

> Vidit: Trust the humanity.



# Maintainer and Acknowledgement
Maintainer: Kaicheng, Vidit.

> Thanks to Zheng Dang for putting up the mac OS installing and basic examples and 
MLO group for their detailed introduction on basic ideas.



