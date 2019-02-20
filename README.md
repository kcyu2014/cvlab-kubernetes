# CVLab Kubernetes Tutorials
EPFL CVLab Kubernetes tutorials with true training examples 🤩

[TODO]
Install kubernetes
* Cite the MLO one.


## Docker part of this.
1. Docker image examples. with correct User permissions.
2. Push to ic-registry.epfl.ch/cvlab/some_projects
3. Examples from IC tutorials including
- ssh from outside.
- mounting cvlabdata2 or other data into the pod.


## Kubernetes part

1. Creation of pods.
  1. A linux pod
  2. With GPU
  3. With GPU and libraries ??

2. Run pod in a correct way
  1. Do not use **sleep and infinity**
  2. Try to debug locally and then deploy
  3. Deploy command examples
  ```bash
  ['python', ... ]
  ```

3. introduction to kubenetes Job
  1. Yaml Job config
  2. Create multiple jobs with hyper-parameter changing with help of `Jinja2`.
  

## Example training FAQs

1. How do I use Tensorboard/Visdom/ .... to monitor my training if I cannot access it like a normal server?

Check the examples in <WILL ADD LATER>.

2. How do I **debug** if I cannot use `sleep infinite`?

Solution 1: Debug on normal server and then deploy. 

Solution 2: Introduce debugging pods


3. How can I run with PyCharm debugger? 

IMPOSSIBLE for now! Or i should say, it's possible but you will not be happy to hear the solution.

4. How do I stop other people eating all the resources

> Victor: Wall of shame. If three strike on the WoS, no GPU for 2 weeks.

> Kaicheng: Please be careful that you live in cvlab for not only a month.

> Vidit: Trust the humanity.





