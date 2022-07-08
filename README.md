# WUGs

Scripts to process Word Usage Graphs (WUGs).

If you use this software for academic research, please [cite](#bibtex) these papers:

- Dominik Schlechtweg, Nina Tahmasebi, Simon Hengchen, Haim Dubossarsky, Barbara McGillivray. 2021. [DWUG: A large Resource of Diachronic Word Usage Graphs in Four Languages](https://aclanthology.org/2021.emnlp-main.567/). In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing.
- Dominik Schlechtweg and Sabine Schulte im Walde. submitted. Clustering Word Usage Graphs: A Flexible Framework to Measure Changes in Contextual Word Meaning.

Find WUG data sets on the [WUGsite](https://www.ims.uni-stuttgart.de/data/wugs).

### Usage

Under `scripts/` we provide a pipeline creating and clustering graphs and extracting data from them (e.g. change scores). Assuming you are working on a UNIX-based system, first make the scripts executable with

	chmod 755 scripts/*.sh

Then run one of the following commands for Usage-Usage Graphs (UUGs) and Usage-Sense Graphs (USGs) respectively:

	bash -e scripts/run_uug.sh
	bash -e scripts/run_usg.sh

__Attention__: modifies graphs iteratively, i.e., current run is dependent on previous run. Script deletes previously written data to avoid dependence.

We recommend you to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.9.5. Install the required packages running `pip install -r requirements.txt`. The script uses simple test parameters; in order to improve the clustering load `parameters_opt.sh` in `run_uug.sh` or `run_usg.sh`.

### Input

 For usage-usage graphs:

- __uses__: find examples at `test_uug/data/*/uses.csv`
- __judgments__: find examples at `test_uug/data/*/judgments.csv`

 For usage-sense graphs:

- __uses__: find examples at `test_usg/data/*/uses.csv`
- __senses__: find examples at `test_usg/data/*/senses.csv`
- __judgments__: find examples at `test_usg/data/*/judgments.csv`

__Note__: The column 'identifier' in each `uses.csv` should identify each word to usage uniquely across all words.

### Description

- `data2join.py`:  joins annotated data
- `data2annotators.py`:  extracts mapping from users to (anonymized) annotators
- `data2agr.py`:  computes agreement on full data
- `use2graph.py`:  adds uses to graph
- `sense2graph.py`:  adds senses to graph, for usage-sense graphs
- `sense2node.py`:  adds sense annotation data to nodes, if available
- `judgments2graph.py`:  adds judgments to graph
- `exclude_nodes.py`:  excludes nodes with many invalid judgments, removes invalid edges
- `graph2cluster.py`:  clusters graph
- `extract_clusters.py`:  extract clusters from graph
- `graph2stats.py`:  extracts statistics from graph, including change scores
- `graph2plot.py`:  plots interactive graph in 2D

Please find the parameters for the current optimized WUG versions in `parameters_opt.sh`. Note that the parameters for the SemEval versions in `parameters_semeval.sh` will only roughly reproduce the published versions, because of non-deterministic clustering and small changes in the cleaning as well as clustering procedure.

For annotating and plotting your own graphs we recommend to use the [DURel Tool](https://www.ims.uni-stuttgart.de/data/durel-tool).

### Additional scripts

- `usim2data.sh`:  downloads USim data and converts it to WUG format

### Further reading

Find further research on WUGs in these papers:

- Frank D. Zamora-Reina, Felipe Bravo-Marquez, Dominik Schlechtweg. 2022. [LSCDiscovery: A shared task on semantic change discovery and detection in Spanish](https://aclanthology.org/2022.lchange-1.16/). In Proceedings of the 3rd International Workshop on Computational Approaches to Historical Language Change.
- Gioia Baldissin, Dominik Schlechtweg, Sabine Schulte im Walde. 2022. DiaWUG: A Dataset for Diatopic Lexical Semantic Variation in Spanish. In Proceedings of the 13th Language Resources and Evaluation Conference.
- Dominik Schlechtweg, Enrique Castaneda, Jonas Kuhn, Sabine Schulte im Walde. 2021. [Modeling Sense Structure in Word Usage Graphs with the Weighted Stochastic Block Model](https://aclanthology.org/2021.starsem-1.23/). In Proceedings of *SEM 2021: The Tenth Joint Conference on Lexical and Computational Semantics.
- Sinan Kurtyigit, Maike Park, Dominik Schlechtweg, Jonas Kuhn, Sabine Schulte im Walde. 2021. [Lexical Semantic Change Discovery](https://aclanthology.org/2021.acl-long.543/). In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers).
- Serge Kotchourko. 2021. [Optimizing Human Annotation of Word Usage Graphs in a Realistic Simulation Environment](https://elib.uni-stuttgart.de/handle/11682/11865). Bachelor thesis.
- Benjamin Tunc. 2021. [Optimierung von Clustering von Wortverwendungsgraphen](https://elib.uni-stuttgart.de/handle/11682/11923). Bachelor thesis.

BibTex
--------

```
@article{Schlechtweg2021dwug,
	title = {{DWUG: A large Resource of Diachronic Word Usage Graphs in Four Languages}},
	author = "Schlechtweg, Dominik and Tahmasebi, Nina and Hengchen, Simon and Dubossarsky, Haim and McGillivray, Barbara",
	year = {2021},
	journal   = {CoRR},
	volume    = {abs/2104.08540},
	archivePrefix = {arXiv},
	eprint    = {2104.08540},
	url = {https://arxiv.org/abs/2104.08540}
}
```
```
@inproceedings{Schlechtweg2021wugs,
	title = {{Clustering Word Usage Graphs: A Flexible Framework to Measure Changes in Contextual Word Meaning}},
	author = {Schlechtweg, Dominik and {Schulte im Walde}, Sabine},
	year = {submitted}
}
```

