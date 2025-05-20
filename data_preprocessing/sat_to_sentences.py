import argparse
import os.path
from tqdm import tqdm
from LiteralContainer_Alice import *
import csv
import pandas as pd


def init():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--dataset', default='dimacs_2sat_15_mixVars_50_mixCls_100K_train', type=str)
    arg_parser.add_argument('--dataset_path', default='dataset/dimacs_files',
                            type=str)
    arg_parser.add_argument('--temp_type', default='or_only', type=str)
    arg_parser.add_argument('--vocabs', default='500', type=str)
    args = arg_parser.parse_args()
    return args


def sat_to_sentence(sat, l_cont, temp_type):
    len_sat = len(sat)
    new_sent = ""
    new_basic_sent = ""
    match len_sat:
        case 1:
            new_sent, new_basic_sent = gen_1sat_sentence(sat, l_cont.list_literals)
        case 2:
            new_sent, new_basic_sent = gen_2sat_sentence(sat, l_cont.list_literals, temp_type)
        case 3:
            new_sent, new_basic_sent = gen_3sat_sentence(sat, l_cont.list_literals, temp_type)
        case 4:
            new_sent, new_basic_sent = gen_4sat_sentence(sat, l_cont.list_literals)
    return new_sent, new_basic_sent


def generate_all_premises(set_premises, l_cont, temp_type):
    sent_main = ""
    sent_basic = ""
    for pm in set_premises:
        new_sent, new_basic_sent = sat_to_sentence(pm, l_cont, temp_type)
        sent_main = sent_main + new_sent + ". "
        sent_basic = sent_basic + new_basic_sent + ". "

    sent_main = sent_main.rstrip(sent_main[-1])
    sent_basic = sent_basic.rstrip(sent_basic[-1])
    return sent_main, sent_basic


def select_template(answer):
    match answer:
        case "hypothesis already exists in the premises":
            return 1
        case "hypothesis can be deduced from the premises":
            return 2
        case "hypothesis contradicts the premises":
            return -1
        case "none can be deduced from the premises":
            return -2
        case "hypothesis contradicts deduced premises":
            return -3
        case "hypothesis can not be deduced from the premises":
            return -4


def calculate_lits(clauses):
    num_lits = 0
    arr_cls = ast.literal_eval(clauses)
    for cls in arr_cls:
        if len(cls) == 1:
            num_lits += 1
    return num_lits


if __name__ == '__main__':
    args = init()

    for mode in ['']:
        f_name = args.dataset + ".csv"
        f_main = os.path.join(args.dataset_path, f_name)
        # args.dataset = args.dataset[:-9]
        f_res_main = os.path.join(args.dataset_path, "sent_" + f_name)

        if args.temp_type == 'easy':
            f_res_main = args.dataset_path + "OD_" + args.dataset + "_" + args.vocabs + "_ER_" + mode + ".csv"
        elif args.temp_type == 'medium':
            f_res_main = args.dataset_path + "OD_" + args.dataset + "_" + args.vocabs + "_MR_" + mode + ".csv"
        elif args.temp_type == 'hard':
            f_res_main = args.dataset_path + "OD_" + args.dataset + "_" + args.vocabs + "_HR_" + mode + ".csv"
        elif args.temp_type == "or_only":
            f_res_main = args.dataset_path + "OD_" + args.dataset + "_" + args.vocabs + "_OR_" + mode + ".csv"

        if os.path.exists(f_res_main):
            print("File is already exists.")

        csv.field_size_limit(100000000)

        df_main = pd.read_csv(f_main, sep=';', engine='python')
        print(len(df_main))

        # fmain = open(f_res_main, "a+")

        with open(f_res_main, "w") as file_main:

            file_main.write(
                "idx;sentence1;sentence2;label;num_atoms;num_clauses;k_hop;breadth;num_lits;steps;new_cl_ratio\n")

            for row in tqdm(df_main.values):

                idx = row[0]
                label = row[3]
                num_atoms = row[4]
                num_clauses = row[5]
                counterexample = row[6]
                k_hop = row[6]
                breadth = row[7]
                steps = row[9]
                num_lits = calculate_lits(row[1])
                new_cl_ratio = row[10]

                ''' --- 1. Translate premises, LC initiation, (sentence1) --- '''
                # print('id: ', idx, 'label: ', label)
                # prem_str = row[1][1:-1]
                prem_str = row[1]
                hyp_str = row[2]
                all_premises = prem_str + "," + hyp_str
                # prem_str = row[1]

                lc = LiteralContainer(all_premises)
                premises = ast.literal_eval(prem_str)

                if isinstance(premises, list):
                    row[1] = row[1] + ','
                    premises = ast.literal_eval(row[1])

                main_sent, main_basic_sent = generate_all_premises(premises, lc, args.temp_type)

                ''' --- 2. Translate muses (sentence2) --- '''
                mus_str = row[2]
                # mus_str = ""
                sent_muses = ""
                sent_basic_mus = ""

                if mus_str:
                    # mus_str = mus_str[1:-1]
                    muses = ast.literal_eval(mus_str)

                    """
                    for mus in muses:
                        sent_mus, sent_basic_mus = sat_to_sentence(mus, lc, args.temp_type)
                        sent_muses += sent_mus + ". "
                    """

                    sent_mus, sent_basic_mus = sat_to_sentence(muses, lc, args.temp_type)

                sent_muses = sent_basic_mus

                # idx;sentence1;sentence2;label;num_atoms;num_clauses;k_hop;breadth;num_lits;steps;new_cl_ratio
                sent_row = str(idx) + ";" + main_basic_sent + ";" + sent_muses + ";" + str(label) + ";" \
                           + str(num_atoms) + ";" + str(num_clauses) + ";" \
                           + str(k_hop) + ";" + str(breadth) + ";" + str(num_lits) + ";" \
                           + str(steps) + ";" + str(new_cl_ratio) + "\n"
                # print(sent_row)
                file_main.write(sent_row)

            file_main.close()
            print("Successfully wrote all entailment pairs.")
