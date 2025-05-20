package edu.clauseentailment;

public class main {

	public static void main(String[] args) {
		double[] probs = {0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5};
		for (double i : probs) {
			int var = 15; /*Determine the maximum number of atom, set 15 as a default.*/
			int min_var = 5; /*Determine the minimum number of atom, set 5 as a default'*/
			int sat = 2; /*Determine the maximum literals for each clause*/
			int min_cls = 2; /*Determine the minimum length of clauses for each instance*/
			int cls = 50; /*Determine the maximum length of clauses for each instance.*/
			int nset = 2000; /*Initiate the number of instances for each generation.*/
			boolean mix_vars = true; /*Set false to generate random number between min_var and var. 
									  Otherwise, set true to set the number of atoms to var.*/
			boolean mix_clauses = false; /*Set false to generate random clauses length between min_cls and cls. 
										   Otherwise, set true to set the clauses length to cls.*/
			String output_dir = "dataset/Entailments_v6/dupl_test/";
			double prob = i;
			var gs = new GenerateSAT_Derivations_v3(sat, var, cls, nset, mix_vars, mix_clauses, output_dir, prob, min_var, min_cls);
			gs.GenerateDataset();
			
		}
		
	}

}
