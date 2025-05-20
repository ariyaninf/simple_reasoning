# There's No Such Thing as Simple Reasoning for LLMs

## Quick links
* [Overview](#overview)
* [SAT Generation](#sat-generation)
* [Data Pre-processing](#data-pre-processing)

## Overview
Large Language Models (LLMs) have been widely found to struggle with logical reasoning, where even fine-tuned models fail dramatically on out-of-distribution problems. However, existing work has focused on relatively complex "many-hop" reasoning problems. In this work, we analyse the performance of fine-tuned LLMs on simple reasoning problems, all of which can be solved in at most three inference steps. Due to the simplicity of these problems, the model cannot encounter test problems that are fundamentally different from those it has seen during training. Unfortunately, however, we find that the models remain highly brittle, being susceptible to seemingly innocent perturbations, such as the addition of duplicates to the set of premises and shuffling the order in which the premises are presented.

This repository provides code implementation and generated dataset for reproducing simple reasoning entailments. We populate all train, validation, and test sets needed in `dataset/` directory, thus generating data from scratch is optional. This directory contains SAT parts as follows:
1. Use `default_train.rar` to fine-tune the models on SAT distribution.
2. `dataset/default_test` contains test scenarios needed to reproduce results in Table 1.
3. To evaluate the impact of duplicate premises on the fine-tuned models or reproduce Figure 2 and Figure 4, use test sets in `dataset/impact_of_duplicates`.
4. Test the fine-tuned models using scenarios in `dataset/impact_of_order` to obtain Figure 3 and Figure 5.
5. `dataset/impact_of_duplicates_order` contains both duplicates and shuffled literals. Use this test to reproduce result in Table 4.
6. As Table 5 shows the impact of verbalization, test the models using `dataset/verbalization_test`.

**Dataset Distribution**

To conduct out-of-distribution test, we implemented two others different dataset distributions: **Rule Priority (RP)** and **Label Priority (LP)**. Please note that we populated the RP and LP test following _SimpleLogic_ in this repository: [Zhang et al., 2022](https://github.com/joshuacnf/paradox-learning2reason)

## SAT Generation
These instructions are optional. Only follow these if you wish to generate the SAT simple propositional entailments from scratch.
1. Download and install SAT4J library from [sat4j.org](https://www.sat4j.org/) to your java IDE.
2. Run `main.java` to generate propositional entailments in dimacs format.   
   
## Data Pre-processing
The following .py files are needed for further data preprocessing starts from dimacs:
* `calculate_depth.py` to calculate the reasoning depth, number of literals, steps, and ratio of new clauses.  
* `data_sampling.py` to uniform sampling based on number of examples and reasoning depth. The bash script below is used to sample 10K instances from previous dimacs file with the same number of population per group. Also note that we will have 8 groups ranging from depth 0 to 3 with a balance positive and negative labels.
   ```
   #!/bin/bash

   python data_sampling.py \
   --dataset_name [dimacs_filename]
   --samples_per_group 1250
   --max_hop 3
   ```
* `sat_to_sentences.py` to translate dimacs formulas into natural sentences. By default, the referred `SATConverter_Alice.py` uses `sr/vocab_500.txt` in df_predicate_list to translate each literal into default list of predicates. Alternatively, we need to modify this source later for setting the verbalization tests.
  - `src/baby-names.txt` to randomize subject names with others,
  - `src/colors_500.txt` to convert default predicates into the list of color names.
