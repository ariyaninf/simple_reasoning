package edu.clauseentailment;

import java.util.Arrays;
import org.sat4j.core.VecInt;
import org.sat4j.minisat.SolverFactory;
import org.sat4j.specs.ContradictionException;
import org.sat4j.specs.ISolver;
import org.sat4j.specs.TimeoutException;

public class ClauseEntailmentChecker {
	
	private final ISolver solver;	
	
	public ClauseEntailmentChecker(final int nVars) {
		this.solver = SolverFactory.newDefault();
		this.solver.newVar(nVars);
		this.solver.setTimeout(Integer.MAX_VALUE);
	}
	
	public void addClause(final int[] dimacsLiterals) throws ContradictionException{
		this.solver.addClause(new VecInt(dimacsLiterals));
	}
	
	public boolean isSatisfiable() {
		try {
			return this.solver.isSatisfiable();
		} catch (TimeoutException e) {
			throw new IllegalStateException("no timeout should occur.");
		}
	}
	
	public boolean isEntailed(final int[] clause) {
		final int[] negClause = Arrays.stream(clause).map(i -> -i).toArray();
		try {
			return !this.solver.isSatisfiable(new VecInt(negClause));
		} catch (TimeoutException e){
			throw new IllegalStateException("no timeout should occur.");
		}
	}
	
	public boolean isSatisfiable(final int[] clause) {
		try {
			return this.solver.isSatisfiable(new VecInt(clause));
		} catch (TimeoutException e) {
			throw new IllegalStateException("no timeout should occur.");
		}
	}
	
}
