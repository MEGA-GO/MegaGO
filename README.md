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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
