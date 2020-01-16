# Mega-GO

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

Mega-GO calculates the similarity between GO terms with the relevance semantic similarity (sim<sub>Rel</sub>) metric
<sup>[1](#myfootnote1)</sup>.

<img src="https://latex.codecogs.com/gif.latex?sim_{rel}(go_1,&space;go_2)&space;=&space;\frac{2\log&space;{&space;(p(l))&space;}&space;}{&space;\log&space;{&space;(go_1)&space;}&space;&plus;&space;\log&space;{&space;(go_2)&space;}&space;}&space;\times&space;(1&space;-&space;p(l))" title="sim_{rel}(go_1, go_2) = \frac{2\log { (p(l)) } }{ \log { (go_1) } + \log { (go_2) } } \times (1 - p(l))" />

where:

 - *l*: lowest common ancestor.
 - *p<sub>1</sub>*: frequency of the term *go<sub>1</sub>*.

The frequency of a term *go* is defined as: 

<img src="https://latex.codecogs.com/gif.latex?p(go)&space;=&space;\frac{n_{go'}}{N}&space;|&space;go'&space;\in&space;\left\{go,&space;c&space;\right\}" title="p(go) = \frac{n_{go'}}{N} | go' \in \left\{go, c \right\}" />

where:

 - *c*: children of *go*.
 - *N*: total number of terms in GO corpus.
 - *n<sub>go'</sub>*: number of occurences of a term *go'* in a reference data set.
 
To calculate the similarity of two sets of terms, the best match average (BMA)<sup>[1](#myfootnote1)</sup> is used.

<img src="https://latex.codecogs.com/gif.latex?SIM_%7BBMA%7D%28g_1%2Cg_2%29%3D%5Cfrac%7B1%7D%7Bm&plus;n%7D*%20%5Cleft%28%20%5Csum_%7B1%3Di%7D%5Em%7B%5Cmax_%7B1%5Cle%20j%5Cle%20n%7D%28sim%28go_%7B1i%7D%2Cgo_%7B2j%7D%29%29%7D&plus;%5Csum_%7B1%3Dj%7D%5En%7B%5Cmax_%7B1%5Cle%20i%5Cle%20m%7D%28sim%28go_%7B1i%7D%2Cgo_%7B2j%7D%29%29%7D%5Cright%29" />

where:
 - *m,n*: number of terms in set *g<sub>i</sub>* and *g<sub>j</sub>*, respectively
 - *sim(go<sub>1i</sub>,go<sub>2j</sub>)*: similarity between two GO terms
 
<a name="myfootnote1">1</a>:  Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for functional similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006) doi:10.1186/1471-2105-7-302

### Interpretation

The relative similarity ranges between 0 and 1. 
  
| *sim(go<sub>1i</sub>,go<sub>2j</sub>) value*   | Interpretation           |
|---------|--------------------------|
| >0.9    | highly similar functions |
| 0.3-0.9 | functionally related     |
| <0.3    | not functionally similar |  

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
