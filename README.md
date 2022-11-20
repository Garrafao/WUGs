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

### Description

- `data2join.py`:  joins annotated data
- `data2annotators.py`:  extracts mapping from users to (anonymized) annotators
- `data2agr.py`:  computes agreement on full data
- `use2graph.py`:  adds uses to graph
- `sense2graph.py`:  adds senses to graph, for usage-sense graphs
- `sense2node.py`:  adds sense annotation data to nodes, if available
- `judgments2graph.py`:  adds judgments to graph
- `graph2cluster.py`:  clusters graph
- `extract_clusters.py`:  extract clusters from graph
- `graph2stats.py`:  extracts statistics from graph, including change scores
- `graph2plot.py`:  plots interactive graph in 2D

Please find the parameters for the current optimized WUG versions in `parameters_opt.sh`. Note that the parameters for the SemEval versions in `parameters_semeval.sh` will only roughly reproduce the published versions, because of non-deterministic clustering and small changes in the cleaning as well as clustering procedure.

For annotating and plotting your own graphs we recommend to use the [DURel Tool](https://www.ims.uni-stuttgart.de/data/durel-tool).

### Additional scripts and data

- `misc/usim2data.sh`:  downloads USim data and converts it to WUG format
- `misc/make_release.sh`: create data for publication from pipeline output (compare to format of published data sets on [WUGsite](https://www.ims.uni-stuttgart.de/data/wugs))
- `durel_system/`: contains files relevant for the [DURel Annotation System](https://www.ims.uni-stuttgart.de/data/durel-tool)

### Input

 For usage-usage graphs:

- __uses__: find examples at `test_uug/data/*/uses.csv`
- __judgments__: find examples at `test_uug/data/*/judgments.csv`

 For usage-sense graphs:

- __uses__: find examples at `test_usg/data/*/uses.csv`
- __senses__: find examples at `test_usg/data/*/senses.csv`
- __judgments__: find examples at `test_usg/data/*/judgments.csv`

__Note__: The column 'identifier' in each `uses.csv` should identify each word usage uniquely across all words.

#### Input Format

The `uses.csv` files must contain one use per line with the following fields specified as header and separated by <TAB>:

	<lemma>\t<pos>\t<date>\t<grouping>\t<identifier>\t<description>\t<context>\t<indexes_target_token>\t<indexes_target_sentence>\n

The CSV files should inlcude one empty line at the end. You can use [this example](https://github.com/Garrafao/WUGs/blob/main/test_uug/data/Vorwort/uses.csv) as a guide (ignore additional columns). The files can contain additional columns including more information such as language, lemmatization, etc.

Find information on the individual fields below:

- __lemma__: the lemma form of the target word in the respective word use
- __pos__: the POS tag if available (else put space character)
- __date__: the date of the use if available (else put space character)
- __grouping__: any string assigning uses to groups (e.g. time-periods, corpora or dialects)
- __identifier__: an identifier unique to each use across lemmas. We recommend to use this format: `filename-sentenceno-tokenno`
- __description__: any additional information on the use if available (else put space character)
- __context__: the text of the use. This will be shown to annotators.
- __indexes\_target\_token__: The *character* indexes of the target token in `context` (Python list ranges as used in slicing, e.g. `17:25`)
- __indexes\_target\_sentence__: The character indexes of the target sentence (containing the target token) in `context` (e.g. `0:30` if context contains only one sentence, or `10:45` if it contains additional surrounding sentences). The part of the context beyond the specified character range will be marked as background in gray.

The `judgments.csv` files must contain one use pair judgment line with the following fields specified as header and separated by <TAB>:

	<identifier1>\t<identifier2>\t<annotator>\t<judgment>\t<comment>\t<lemma>\n

The CSV files should inlcude one empty line at the end. You can use [this example](https://github.com/Garrafao/WUGs/blob/main/test_uug/data/Vorwort/judgments.csv) as a guide (ignore additional columns). The files can contain additional columns including more information such as the round of annotation, etc.

Find information on the individual fields below:

- __identifier1__: identifier of the first use in the use pair (must correspond to identifier in uses.csv)
- __identifier2__: identifier of the second use in the use pair
- __annotator__: annotator name
- __judgment__: annotator judgment on graded scale (e.g. 1 for unrelated, 4 for identical)
- __comment__: the annotator's comment (if any)
- __lemma__: the lemma form of the target word in both uses

### Further reading

Find further research on WUGs in these papers:

- Anna Aksenova, Ekaterina Gavrishina, Elisey Rykov, and Andrey Kutuzov. 2022. [Rudsi: graph-based word sense induction dataset for russian](https://arxiv.org/abs/2209.13750).
- Frank D. Zamora-Reina, Felipe Bravo-Marquez, Dominik Schlechtweg. 2022. [LSCDiscovery: A shared task on semantic change discovery and detection in Spanish](https://aclanthology.org/2022.lchange-1.16/). In Proceedings of the 3rd International Workshop on Computational Approaches to Historical Language Change.
- Gioia Baldissin, Dominik Schlechtweg, Sabine Schulte im Walde. 2022. [DiaWUG: A Dataset for Diatopic Lexical Semantic Variation in Spanish](https://aclanthology.org/2022.lrec-1.278/). In Proceedings of the 13th Language Resources and Evaluation Conference.
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

