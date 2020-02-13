# Code release for the ICRA 2020 paper "Topological Mapping for Manhattan-like Repetitive Environments"

Sai Shubodh Puligilla\*, Satyajit Tourani\*, Tushar Vaidya\*, Udit Singh Parihar\*, Ravi Kiran Sarvadevabhatla and K. Madhava Krishna

> Links to [**Paper**]() and [**Video**]()

# Introduction

We showcase a topological mapping framework for a challenging indoor warehouse setting. At the most abstract level, the warehouse is represented as a Topological Graph where the nodes of the graph represent a particular warehouse topological construct (e.g. rackspace, corridor) and the edges denote the existence of a path between two neighbouring nodes or topologies. At the intermediate level, the map is represented as a Manhattan Graph where the nodes and edges are characterized by Manhattan properties and as a Pose Graph at the lower-most level of detail. The topological constructs are learned via a Deep Convolutional Network while the relational properties between topological instances are learnt via a Siamese-style Neural Network. In the paper, we show that maintaining abstractions such as Topological Graph and Manhattan Graph help in recovering an accurate Pose Graph starting from a highly erroneous and unoptimized Pose Graph. We show how this is achieved by embedding topological and Manhattan relations as well as Manhattan Graph aided loop closure relations as constraints in the backend Pose Graph optimization framework. The recovery of near ground-truth Pose Graph on real-world indoor warehouse scenes vindicate the efficacy of the proposed framework.

<p align="center">
    <img src="assets/pipeline.png" />
</p>


# Citation:
 
If you find our work useful in your research, please consider citing:
```

```