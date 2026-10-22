# Gap-hunt: Theorem 11.38 (note_v3.md §11.4), 2026-10-21

Verdict: proof structure correct; one concrete defect in the stated constants.

## Defect [computer-assisted, reproducible]
Table under Thm 11.38 prints `theta_3 <= 0.22940`. Exact value (closed form, p=3: Gamma_3(1)=1/32, J0=2):
theta_3 = (2/3)[(2/3)log_3(33/32) + (1/3)(log_3(3/16)+1) + (1/3)(3/2)] = 0.2294000282861937...
> 0.22940. The author's own interval output (T3a data/theta.txt) says 2.294000283e-01; the note truncated
instead of rounding up. The proof gives slope 0.22940003, and the excess 2.8e-8*k is not O(log^2 k), so the
printed inequality is unproved (not shown false). Fix: print 0.22941 (or 0.2294001). All other printed
bounds (p=2,5,7,11,13,17,19 and the 1-theta_set row) are correctly rounded in the safe direction.

## Independent recomputation
code/indep_theta.py (own DP over integer values of W, exact Fractions, mpmath 50 digits; did not reuse
gamma_enum/theta.py). p<=17: Gamma_p(1), J0, L_p, theta_p, 1-theta_set agree with note to all printed digits;
closed-form tail cross-checked against a 400-term direct sum. p=19 run killed after >10 min (dict DP slow);
p=19 relies on authors' gamma_enum.c + theta.py. Log: indep_theta.log.

## Line-by-line check of the proof
- Block/level structure: x_{pm+r}/p^a = U_m P_m(r), pm+i = p(m+1)-(p-i) == -(p-i) mod p^{J_m},
  so P_m(r) == (-1)^r (p-1)!/(p-1-r)! = eps_p e_{p-1-r}. Re-derived directly (does not need Thm 3.9). OK, incl. p=2.
- Thm 11.36(ii),(iv) applied with j<=J (j=J_m for m<M, j=k-a_M<=J_M since a_{M+1}>=k). kappa-hat>=0 real from (i);
  rho-hat in [0,1]; D<=Gamma. OK.
- Gamma_p nondecreasing (sum of nonneg terms over growing frequency set). OK.
- Partial first group when p does not divide N_0: level 0, jump v_p(p m_0)=1+v_p(m_0), trivial factor p^j. OK.
- Counting floor(X/p^j)-floor(X/p^{j+1}) <= X(1-1/p)p^{-j}+1, f_p(j)<=j+1 => error <= (L+1)(L+2)/2 <= (log_p X+2)^2/2. OK.
- e_M=(pM-s_p(M))/(p-1) < k+e_0 => M+1 <= (p-1)/p (k+e_0+log_p M+O(1)); theta_p=(p-1)/p F_p matches definition. OK.
- Minor wording: A_p independent of N_0 needs (log(k+e_0))^2 <= 2log^2 k + 2log^2(1+e_0); fine but unstated.
- theta_2 = log_2(3)/4 re-derived by hand (Gamma_2(1)=0, Gamma_2(j)=3*2^j/8-1, j>=2). OK.
