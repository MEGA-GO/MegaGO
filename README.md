# MegaGO

![](doc/logo.png)

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

### Installing

Clone the repository:

```shell script
git clone https://github.com/MEGA-GO/Mega-Go.git
```

Install package:

```shell script
cd Mega-Go
pip install -U .
```

Execute example analysis:

```shell script
megago functional_tests/testdata/example_input-compare_goa.csv
```

## How does it work?

MegaGO calculates the similarity between GO terms with the relevance semantic similarity (sim<sub>Rel</sub>) metric
<sup>[1](#myfootnote1)</sup>.

<img src="https://latex.codecogs.com/svg.latex?sim_{lin}(go_1,%20go_2)%20=%20\frac{2IC(MICA)}{%20IC%20(go_1)%20%20+%20IC%20(go_2)%20}" />

where:

 - *MICA*: most informative common ancestor.
 - *IC(go<sub>i</sub>)*: information content of the term *go<sub>i</sub>*.

The information content of a go term is calculated as follows: <img src="https://latex.codecogs.com/svg.latex?IC(go_i)%20=%20\log{p(go_i)}" />

The frequency *p* of a term *go* is defined as: 

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
 
<a name="myfootnote1">1</a>: Lin, Dekang. 1998. “An Information-Theoretic Definition of Similarity.” In Proceedings of the 15th International Conference on Machine Learning, 296—304.

### Interpretation

The relative similarity ranges between 0 and 1. 
  
| *sim(go<sub>1i</sub>,go<sub>2j</sub>) value*   | Interpretation           |
|---------|--------------------------|
| >0.9    | highly similar functions |
| 0.3-0.9 | functionally related     |
| <0.3    | not functionally similar |  

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
