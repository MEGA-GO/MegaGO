# Mega-Go


## How does it work?

Mega-Go useses relevance semantic similarity similarity for GO terms (**s**) (Schlicker, A., Domingues, F.S., Rahnenführer, J. et al. A new measure for functional similarity of gene products based on Gene Ontology. BMC Bioinformatics 7, 302 (2006) doi:10.1186/1471-2105-7-302).

<img src="https://latex.codecogs.com/gif.latex?s(t_1,&space;t_2)&space;=&space;\frac{2\log&space;{&space;(p(l))&space;}&space;}{&space;\log&space;{&space;(t_1)&space;}&space;&plus;&space;\log&space;{&space;(t_2)&space;}&space;}&space;\times&space;(1&space;-&space;p(l))" title="s(t_1, t_2) = \frac{2\log { (p(l)) } }{ \log { (t_1) } + \log { (t_2) } } \times (1 - p(l))" />

**l**: lowest common ancestor


