# There's No Such Thing as Simple Reasoning for LLMs

## Quick links
* [Overview](#Overview)

## Overview
Large Language Models (LLMs) have been widely found to struggle with logical reasoning, where even fine-tuned models fail dramatically on out-of-distribution problems. However, existing work has focused on relatively complex "many-hop" reasoning problems. In this work, we analyse the performance of fine-tuned LLMs on simple reasoning problems, all of which can be solved in at most three inference steps. Due to the simplicity of these problems, the model cannot encounter test problems that are fundamentally different from those it has seen during training. Unfortunately, however, we find that the models remain highly brittle, being susceptible to seemingly innocent perturbations, such as the addition of duplicates to the set of premises and shuffling the order in which the premises are presented.

This repository provides code implementation and generated dataset for reproducing simple reasoning entailments. We populate all train, validation, and test sets needed in `dataset/` directory, thus generating data from scratch is optional. This directory contains parts as follows:
1. Use `default_train.rar` to fine-tune the models on SAT distribution.
2. `dataset/default_test` contains test scenarios needed to reproduce results in Table 1.
3. To evaluate the impact of duplicate premises on the fine-tuned models or reproduce Figure 2 and Figure 4, use test sets in `dataset/impact_of_duplicates`.
4. Test the fine-tuned models using scenarios in `dataset/impact_of_order` to obtain Figure 3 and Figure 5.
5. `dataset\impact_of_duplicates_order` contains both duplicates and shuffled literals. Use this test to reproduce result in Table 4.
6. As Table 5 shows the impact of verbalization, test the models using `dataset/verbalization_test`.

## Requirements

## Data Preprocessing

## Train the model
