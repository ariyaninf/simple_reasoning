package edu.clauseentailment;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

import org.sat4j.specs.ContradictionException;

public class GenerateSAT_Derivations_v3 {
	
	private final int NVAR;
	private final int MIN_NVAR;
	private final int KSAT;
	private final int NCLAUSE;
	private final int MIN_NCLAUSE;
	private int NSET;
	private boolean IS_MIXVARS;
	private boolean IS_MIXCLAUSES;
	private final String fname;
	private final String output_dir;
	private static double PROBABILITY;
	
	public GenerateSAT_Derivations_v3(final int i_ksat, final int i_nvar, final int i_nclause, final int i_nset, 
			final boolean i_isMixVars, final boolean i_isMixClauses, final String output_dir, double i_prob, int i_minvars,
			int i_min_cls) {
		this.NVAR = i_nvar;
		this.MIN_NVAR = i_minvars; //15
		this.KSAT = i_ksat;
		this.NCLAUSE = i_nclause;
		this.MIN_NCLAUSE = i_min_cls;
		this.NSET = i_nset;
		this.IS_MIXVARS = i_isMixVars;
		this.IS_MIXCLAUSES = i_isMixClauses;
		this.output_dir = output_dir;
		this.PROBABILITY = i_prob;
		
		if (!this.IS_MIXVARS && !this.IS_MIXCLAUSES) {
			this.fname = this.output_dir + KSAT + "sat_" + NVAR + "_fixVars_" + NCLAUSE + "_fixCls_" + PROBABILITY + "_" + NSET + "_def.csv";
		} else if (!this.IS_MIXVARS && this.IS_MIXCLAUSES) {
			this.fname = this.output_dir + KSAT + "sat_" + NVAR + "_fixVars_" + NCLAUSE + "_mixCls_" + PROBABILITY + "_" + NSET + "_def.csv";
		} else if (this.IS_MIXVARS && !this.IS_MIXCLAUSES) {
			this.fname = this.output_dir + KSAT + "sat_" + NVAR + "_mixVars_" + NCLAUSE + "_fixCls_" + PROBABILITY + "_" + NSET + "_def.csv";
		} else {
			this.fname = this.output_dir + KSAT + "sat_" + NVAR + "_mixVars_" + NCLAUSE + "_mixCls_" + PROBABILITY + "_" + NSET + "_def.csv";
		}
		
	}
	
	public int RandomLiteral(int NVAR) {
		int randomNum = 0;
		while(randomNum == 0) {
			randomNum = ThreadLocalRandom.current().nextInt(- NVAR, NVAR);
		}
		return randomNum;
	}
	
	public boolean IsExists (int[] clause1, List<int[]> clauses) {
		boolean flag = false;
		Arrays.sort(clause1);
		for (int[] elem : clauses) {
			Arrays.sort(elem);
			if (Arrays.equals(clause1, elem)) {
				flag = true;
			}
		}
		return flag;
	}
	
	public static int generateRandomSATWithProbability(int KSAT) {
        double randomValue = Math.random();
        switch (KSAT) {
        case 2:
        	if (randomValue <= PROBABILITY) {
                return 1;
            } else {
                return 2;
            }
        case 3:
        	if (randomValue < 0.3) {
                return 1;
            } else if (randomValue >= 0.3 && randomValue < 0.7){
                return 2;
            } else {
            	return 3;
            }
        }
		return 0;        
    }
	
	
	public int[] GenerateClause (int KSAT, int NVAR, List<int[]> clauses) {
		//int len_sat = ThreadLocalRandom.current().nextInt(1, KSAT + 1); //uncomment this to mix the SAT
		//int len_sat = KSAT;  //uncomment this to fix the SAT
		int len_sat = generateRandomSATWithProbability(KSAT);
		int[] clause = new int[len_sat];
		boolean is_exists = true;
		
		while (is_exists) {			
			for (int j=0; j < len_sat ; j++) {
				int flag = 1;
				while (flag == 1) {
					flag = 0;
					int lit = RandomLiteral(NVAR);
						
					for (int k=0; k < len_sat; k++) {
						if (Math.abs(clause[k]) == Math.abs(lit)) {
							flag = 1;
						}
					}
					if (flag==0) {
						clause[j] = lit;
					}
				}
			}
			
			if (!IsExists(clause,clauses)) {
				is_exists = false;
			} 
		}
		return clause;
	}
	
	public int[] GenerateHypo (int KSAT, int NVAR) {
		//int len_sat = ThreadLocalRandom.current().nextInt(1, KSAT + 1);  //uncomment this to mix SAT
		int len_sat = 1;  //uncomment this to fix the SAT = 1
		
		int[] hypo = new int[len_sat];

		for (int j=0; j < len_sat ; j++) {
			int lit = RandomLiteral(NVAR);
			hypo[j] = lit;
		}
		
		return hypo;
	}
	
	public String ConcateArrayClauses (List<int[]> cls) {
		String concat = new String();
		for (int[] c : cls) {
			concat = concat + Arrays.toString(c) + ",";
		}
		return concat.substring(0, concat.length() - 1);
	}	
	
	public void GenerateDataset()  {
		int num_total_pos = NSET / 2;
		int num_total_neg = num_total_pos;
		int count_pos = 0;
		int count_neg = 0;
		int id = 1;
		int numClauses = 0;
		int numVars = 0;
		
		try {
			PrintWriter writer = new PrintWriter(fname, "UTF-8");
			writer.println("id;clauses;queries;label;num_vars;num_clauses");
			String premise_clause = new String();
			
			while(id <= NSET) {
				boolean flag_gen = true;

				var mainChecker = new ClauseEntailmentChecker(NVAR);
				List<int[]> clauses = new ArrayList<>();
				
				while (flag_gen)
				{
					mainChecker = new ClauseEntailmentChecker(NVAR);
					boolean numCls_error = true;
					while (numCls_error) {
						/* HINT: Initiate the number of clauses */
						if (IS_MIXCLAUSES) {
							numClauses = ThreadLocalRandom.current().nextInt(MIN_NCLAUSE, NCLAUSE + 1);
						} else {
							numClauses = NCLAUSE;
						}
						
						/* HINT: Initiate the number of variables */
						if (IS_MIXVARS) {
							numVars = ThreadLocalRandom.current().nextInt(MIN_NVAR, NVAR + 1);
						} else {
							numVars = NVAR;
						}
						
						if (numClauses < numVars * 5) {
							numCls_error = false;
						}
					}
					
					//System.out.println("numClauses: " + numClauses);
					//System.out.println("numVars: " + numVars);
					
					clauses = new ArrayList<>();
					int count = 0;
					
					while (clauses.size() < numClauses && flag_gen && count < 1000) {
			
						int[] clause = new int[KSAT];					
						clause = GenerateClause(KSAT, numVars, clauses);
						
						//System.out.println("clause: " + Arrays.toString(clause));
						
						clauses.add(clause);
						try {
							if (mainChecker.isSatisfiable(clause)) {
								mainChecker.addClause(clause);
							} else {
								clauses.remove(clauses.size()-1);
								count += 1;
							}				
						} catch (ContradictionException e) {
							clauses.remove(clauses.size()-1);
							count += 1;
						}
						
						if (count == 1000 || clauses.size() == numClauses) {
							flag_gen = false;
							//System.out.println(flag_gen + " " + clauses.size());
						}
						
					}
							
				}
				
				if (!flag_gen) {
					/* Generate hypothesis */
					int[] hyp = GenerateHypo(KSAT, numVars);
					
					try {
						if (mainChecker.isEntailed(hyp)) {
							if (count_pos < num_total_pos) {
								premise_clause = id + ";" + ConcateArrayClauses(clauses) + ";" + Arrays.toString(hyp) + ";" + "1" + ";" + numVars + ";" + numClauses;
								System.out.println(premise_clause);
								writer.println(premise_clause);
								count_pos += 1;
								id += 1;
							}
						} else {
							if (count_neg < num_total_neg) {
								premise_clause = id + ";" + ConcateArrayClauses(clauses) + ";" + Arrays.toString(hyp) + ";" + "0" + ";" + numVars + ";" + numClauses;
								System.out.println(premise_clause);
								writer.println(premise_clause);
								count_neg += 1;
								id += 1;
							}
						}
					} catch (IllegalStateException e) {
						System.out.println("An error is occured in generating examples.");
					}
				}
				
			}
			
			writer.close();
			System.out.println("Successfully wrote to the file.");
		} catch(IOException e){
			System.out.println("An error occured.");
			e.printStackTrace();
		}
	}

}
