# Upload formats for DURel system
## Overview
In order to create a new project, you have three options:
1.	You can upload use csv. The system will automatically create use pairs for each CSV. These pairs will be shown to the users as part of the annotation process. 

2.	You can upload use csv and instance csv. In this case, the users upload the pair they want to annotate and then these pre-selected pairs would be shown to the users in the annotation process.

3.	You can upload use csv and judgment csv. In this case, the use pairs are already annotated, the users could use the system for visulization.
You are allowed to upload as many CSV files as you want in one single project (Use CTRL to select multiple files). Note in the second and third option, the number of use csv should match the number of instance/judgment csv.

## Uses

The `uses.csv` files must contain __one use per line__ with the following fields specified as header and separated by <TAB>:

	<lemma>\t<pos>\t<date>\t<grouping>\t<identifier>\t<description>\t<context>\t<indexes_target_token>\t<indexes_target_sentence>\n

The CSV files should include one empty line at the end (this is the standard in general). Each CSV file must contain only the uses of one word. You can find examples under `test_uug/uses/`.

Find information on the individual fields below:

* __lemma__: the lemma form of the target word in the respective word use
* __pos__: the POS tag if available (else put space character)
* __date__: the date of the use if available (else put space character)
* __grouping__: any string assigning uses to groups (e.g. time-periods, corpora or dialects)
* __identifier__: an identifier unique to each use across lemmas. We recommend to use this format: `filename-sentenceno-tokenno`
* __description__: any additional information on the use if available (else put space character)
* __context__: the text of the use. This will be shown to annotators.
* __indexes\_target\_token__: The *character* indexes of the target token in `context` (Python list ranges as used in slicing, e.g. `17:25`)
* __indexes\_target\_sentence__: The character indexes of the target sentence (containing the target token) in `context` (e.g. `0:30` if context contains only one sentence, or `10:45` if it contains additional surrounding sentences). The part of the context beyond the specified character range will be marked as background in gray.

## Instances

The `instances.csv` files must contain __one use pair per line__ with the following fields specified as header and separated by <TAB>:

	<lemma>\t<identifier2>\t<identifier1>\n

The CSV files should inlcude one empty line at the end. Each CSV file must contain only the instances of one word. You can find examples under `test_uug/instances/`.

Find information on the individual fields below:

- __lemma__: the lemma form of the target word in both uses
- __identifier1__: identifier of the first use in the use pair (must correspond to identifier in uses.csv)
- __identifier2__: identifier of the second use in the use pair


## Judgments

The `judgments.csv` files must contain __one use pair judgment per line__ with the following fields specified as header and separated by <TAB>:

	<identifier1>\t<identifier2>\t<annotator>\t<judgment>\t<comment>\t<lemma>\n

The CSV files should inlcude one empty line at the end. Each CSV file must contain only the judgments of one word. You can find examples under `test_uug/judgments/`.

Find information on the individual fields below:

- __identifier1__: identifier of the first use in the use pair (must correspond to identifier in uses.csv)
- __identifier2__: identifier of the second use in the use pair
- __annotator__: annotator name
- __judgment__: annotator judgment on graded scale (e.g. 1 for unrelated, 4 for identical)
- __comment__: the annotator's comment (if any)
- __lemma__: the lemma form of the target word in both uses
