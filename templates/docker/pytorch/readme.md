# Pytorch Docker file

Note this file relies on the Nvidia official docker images built for pytorch.

You could change this `FROM nvcr.io/nvidia/pytorch:xx.xx-py3` line to a different version.
For more versions and detailed documentation, please visit this site [NVIDIA-NGC-document](https://docs.nvidia.com/deeplearning/frameworks/pytorch-release-notes/rel_19-10.html#rel_19-10). 


For example, `pytorch:18:09-py3` means this is a 2018 September release with python 3 pre-installed as default.
It is using `pytorch==0.4.1+`.

Some commonly used pytorch repo:

NGC tag | Pytorch version
----| ---
`19.10` | PyTorch 1.3.0a0+24ae9b5
`19.09` | PyTorch 1.2.0
`18.09` | PyTorch 0.4.1+ 



