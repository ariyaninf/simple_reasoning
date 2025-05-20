import pandas as pd
import argparse
import os.path


def init():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--dataset_name', default='inferred_2sat_15_mixVars_40_mixCls_13k_clean_val',
                             type=str)
    args_parser.add_argument('--dataset_path', default='dataset/dimacs_files',
                             type=str)
    args_parser.add_argument('--samples_per_group', default=1250, type=int)
    args_parser.add_argument('--max_hop', default=3, type=int)
    args_parser.add_argument('--random_seed', default=123, type=int)
    arguments = args_parser.parse_args()
    return arguments


if __name__ == '__main__':

    args = init()

    # Load the dataset
    f_main = os.path.join(args.dataset_path, args.dataset_name + ".csv")
    df = pd.read_csv(f_main, sep=';', engine='python', encoding='latin-1')

    # Filter where k_hop < 4
    filtered_df = df[df['k_hop'] <= args.max_hop]
    n_samples_per_group = args.samples_per_group

    # Ensure that all instances are unique within the groups
    def unique_sample(group, n_samples_per_group):
        # If the group has fewer rows than n_samples_per_group, we will duplicate the group
        n_rows = len(group)
        if n_rows >= n_samples_per_group:
            return group.sample(n=n_samples_per_group, replace=False, random_state=args.random_seed)
        else:
            # If the group has fewer rows, we duplicate unique samples until we reach n_samples_per_group
            full_group = pd.concat([group] * (n_samples_per_group // n_rows), ignore_index=True)
            remaining_samples = group.sample(n=n_samples_per_group % n_rows, replace=False, random_state=args.random_seed)
            return pd.concat([full_group, remaining_samples], ignore_index=True)

    # Apply the unique sampling for each group
    uniform_sampled_df = filtered_df.groupby(['label', 'k_hop']).apply(
        lambda x: unique_sample(x, n_samples_per_group)
    ).reset_index(drop=True)

    print(uniform_sampled_df)

    # Shuffle the sampled DataFrame
    uniform_sampled_df = uniform_sampled_df.sample(frac=1, random_state=args.random_seed).reset_index(drop=True)

    # Save to a new CSV file
    fname = os.path.join(args.dataset_path, args.dataset_name + "_balanced.csv")
    uniform_sampled_df.to_csv(fname, sep=';', encoding='utf-8', index=False)
