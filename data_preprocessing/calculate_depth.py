import argparse
import ast
import csv
import os
from os.path import isfile, join
from os import listdir

import pandas as pd
from tqdm import tqdm


def init():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--dataset_path', default="dataset/dimacs_files",
                            type=str)
    arg_parser.add_argument('--max_steps', default=40000, type=int)
    args = arg_parser.parse_args()
    return args


def is_tautology(clause):
    if len(clause) > 1:
        if clause[0] == -clause[1]:
            return True
        else:
            return False
    else:
        False


def resolve(c1, c2):
    resolvent_literals = []
    if not is_tautology(c1[0]) and not is_tautology(c2[0]):
        for literal in c1[0]:
            if -literal in c2[0]:
                resolvent_literals = [lit for lit in c1[0] + c2[0] if lit != literal and lit != -literal]
                # resolvents.append(tuple(set(resolvent_literals)))  # Convert list to tuple
    elif is_tautology(c1[0]):
        resolvent_literals = c2[0]
    elif is_tautology(c2[0]):
        resolvent_literals = c1[0]

    resolvent_literals = sorted(set(resolvent_literals))
    depth = c1[1] + c2[1] + 1
    # resolvent_literals.sort()
    return resolvent_literals, depth


def is_fact(clause):
    if len(clause) == 1:
        return True
    else:
        return False


def check_entailment(input_list, hypo):
    '''
    # Find the minimum pair value for the query or return None if not found
    min_value = min((value for items, value in input_list if items == hypo), default=None)

    if min_value is None:
        return False, min_value
    else:
        return True, min_value
    '''

    # Flatten hyp to make comparison easier
    hyp_flattened = [item for sublist in hypo for item in sublist]

    # Iterate through arr_clauses to find a match
    for clause, value in input_list:
        if set(hyp_flattened) == set(clause):
            return True, value

    # Return None if no match is found
    return False, max(value for _, value in input_list)


def is_exist_resolvent(input_list, resolvent, depth):
    new_tuple = (resolvent, depth)
    if new_tuple in input_list:
        return True
    else:
        return False


def is_set_subset_of_list(subset, main_list):
    for x in main_list:
        tuple_list = [tuple(x) for x in main_list]

    # Check if every element in subset is in the tuple_list
    return all(item in tuple_list for item in subset)


def resolution_steps(premises, hypothesis, max_steps):
    # contain all facts from prior set of premises and inferred facts
    arr_clauses = []

    # add all clauses in premises to arr_clauses
    for clause in premises:
        clause = sorted(set(clause))
        arr_clauses.append((clause, 0))

    arr_steps = []
    new_arr_clauses = []
    # new = set()

    count_steps = 0
    iter = 0

    is_entailed, entailment_depth = check_entailment(arr_clauses, hyp)
    if is_entailed:
        return is_entailed, arr_steps, arr_clauses, entailment_depth, count_steps

    while True:
        iter += 1
        new = []

        if not new_arr_clauses:
            pairs = [(arr_clauses[i], arr_clauses[j]) for i in range(len(arr_clauses))
                     for j in range(i + 1, len(arr_clauses))]
        else:
            # arr_clauses = arr_clauses + new_arr_clauses
            pairs = [(arr_clauses[i], new_arr_clauses[j]) for i in range(len(arr_clauses))
                     for j in range(len(new_arr_clauses))]

        new_arr_clauses = []

        for (ci, cj) in pairs:
            resolvents, depth = resolve(ci, cj)
            count_steps += 1

            if resolvents:  # resolvents are not empty
                if not is_exist_resolvent(arr_clauses, resolvents, depth):
                    new.append((resolvents, depth))
                    arr_steps.append((ci, cj, (resolvents, depth)))
                new_arr_clauses.append((resolvents, depth))

            # if len(arr_steps) > max_steps:
            if count_steps > max_steps:
                arr_clauses = arr_clauses + new_arr_clauses
                is_entailed, entailment_depth = check_entailment(arr_clauses, hyp)
                return is_entailed, arr_steps, arr_clauses, entailment_depth, count_steps

        # print(new_arr_clauses)
        # printResolutionPath(arr_steps)
        arr_clauses = arr_clauses + new_arr_clauses

        is_entailed, entailment_depth = check_entailment(arr_clauses, hyp)
        if is_entailed:
            return is_entailed, arr_steps, arr_clauses, entailment_depth, count_steps

        if not new:
            return is_entailed, arr_steps, arr_clauses, entailment_depth, count_steps


def printResolutionPath(in_steps):
    path = ""
    if in_steps:
        for step in in_steps:
            path += f"{step[0]} ∨ {step[1]} -> {step[2]}\n"
    else:
        path += "No resolutions found."
    return path


def printCounterexample(examples):
    if examples:
        print("Counterexample:")
        print(examples)
    else:
        print("No counterexample found.")


def calculateLiterals(premises):
    count_lit = 0
    for p in premises:
        if len(p) == 1:
            count_lit += 1
    return count_lit


if __name__ == '__main__':
    args = init()

    only_dimacs_files = [f for f in listdir(args.dataset_path) if isfile(join(args.dataset_path, f)) and
                         f.endswith(".csv")]

    sorted_files = sorted(only_dimacs_files)

    for f in sorted_files:
        print(f)
        f_dimacs = os.path.join(args.dataset_path, f)
        dataset_name = f

        csv.field_size_limit(100000000)
        df_dimacs = pd.read_csv(f_dimacs, sep=';', engine='python')

        result_path = os.path.join(args.dataset_path)
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        else:
            print("New folder is exists.")

        f_res_main = os.path.join(result_path, "inferred_" + dataset_name)
        f_counter_main = os.path.join(result_path, "cex_" + dataset_name)
        f_exp_main = os.path.join(result_path, "exp_" + dataset_name[:-4] + ".txt")

        with open(f_res_main, "w") as file_res, open(f_counter_main, "w") as file_cex, \
                open(f_exp_main, "w", encoding="utf-8") as file_exp:
            file_res.write(
                "idx;sentence1;sentence2;label;num_atoms;num_clauses;k_hop;breadth;num_lits;steps;new_cl_ratio\n")
            file_cex.write("idx;label;num_atoms;num_clauses;counterexamples\n")

            # idx;sentence1;sentence2;label;num_atoms;num_clauses;num_lits;clauses;queries
            for index, row in df_dimacs.iterrows():
                idx = row['idx']
                sentence1 = ast.literal_eval(row['clauses'])
                sentence2 = ast.literal_eval(row['queries'])
                num_atoms = row['num_atoms']
                num_clauses = row['num_clauses']
                clauses = sentence1
                hyp = sentence2

                entailment_label, steps, inferred_clauses, hops, num_steps = resolution_steps(clauses, hyp,
                                                                                              args.max_steps)

                breadth = len(inferred_clauses)
                literals = calculateLiterals(clauses)
                ratio = round((breadth - num_clauses) / num_clauses, 2)

                row_sent = f"{idx};{sentence1};{sentence2};{entailment_label};{num_atoms};" \
                           f"{num_clauses};{hops};{breadth};{literals};{num_steps};{ratio}\n"

                row_cex = f"{idx};{entailment_label};{num_atoms};{num_clauses};{inferred_clauses}\n"
                row_cex = str(idx) + ";" + str(int(entailment_label)) + ";" + str(num_atoms) + ";" + str(num_clauses) \
                          + ";" + str(inferred_clauses) + "\n"

                row_exp = f"idx: {idx}\n" \
                          f"Premises: {sentence1}\n" \
                          f"Hypothesis: {sentence2}\n\n" \
                          f"Derivations:\n{printResolutionPath(steps)}" \
                          f"\n-----------------------------------\n\n"

                # print(idx)
                # printResolutionPath(steps)

                file_res.write(row_sent)
                file_cex.write(row_cex)
                file_exp.write(row_exp)

            file_res.close()
            file_cex.close()
            file_exp.close()
