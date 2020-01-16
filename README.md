# Mega-Go

Calculate semantic distance for sets of Gene Ontology terms.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Scripts are written in python 3. One easy way to get started is installing 
[miniconda 3](https://docs.conda.io/en/latest/miniconda.html).

On linux:

```shell script
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Install goatools and jupyter:

```shell script
conda install goatools jupyter
```

### Installing

Clone the repository:

```shell script
git clone https://github.com/MEGA-GO/Mega-Go.git
```

Download GO ressource data to working dir:

```shell script
cd Mega-Go
wget http://geneontology.org/ontology/go-basic.obo
```

Execute notebook:

```shell script
jupyter similarty_metrics.ipynb
```

## How does it work?

Mega-Go useses relevance semantic similarity similarity for GO terms (**s**) (Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for functional similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006) doi:10.1186/1471-2105-7-302).

<img src="https://latex.codecogs.com/gif.latex?s(t_1,&space;t_2)&space;=&space;\frac{2\log&space;{&space;(p(l))&space;}&space;}{&space;\log&space;{&space;(t_1)&space;}&space;&plus;&space;\log&space;{&space;(t_2)&space;}&space;}&space;\times&space;(1&space;-&space;p(l))" title="s(t_1, t_2) = \frac{2\log { (p(l)) } }{ \log { (t_1) } + \log { (t_2) } } \times (1 - p(l))" />

**l**: lowest common ancestor


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
