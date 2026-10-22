# Gap-hunt: Corollary 11.20 (note_v3.md, sec. 11.2), 2026-10-21
Verdict: NOT refuted. Severity of issues found: minor (wording only).

Chain checked line by line:
1. dim_H <= lower box dim for bounded sets [standard]; box count at scale p^-G in Z_p = #classes mod p^G meeting K_p. So N(G) >= p^{(D-eps)G} for large G. OK.
2. Each class meeting K_p lies in {g_p>=G}: Theorem 3.1(a)/(b) (S_B in Z[x]). delta_G = p^-G #{c: g_p(c)>=G} (Thm 3.1(c)). So delta_G >= p^{-(1-D+eps)G}. OK.
3. dim_H K_p >= D_p(w,K): Theorem 11.17 needs a simple zero alpha != -2 of a finite-support word. Exists for every p: Prop 11.13(b) x_c, v(x_c+2)=v(c!)<inf. Hypothesis p !| w holds for (2,9,22). Re-checked: (11.2) distance formula (bracket uses q^z_s = q_s(tau_k) mod p^K, G_k<=K; tail >= L_{k+1} = L_k+g_k >= L_k+G_k; Lemma 11.12(b) applicable since v(z-z')>=P_0>lambda; e^J=e+1_J as flips are beyond support), cylinder/ball identification and constancy of rho_k on cylinders, (11.3), equidistribution of tau_m/p mod p^{K-1} (p !| w), denominator bound sum v(z+n) <= T/(p-1)+M, Lemma 11.18 Steps A-C (F2 uses p^{beta+1}>P; Step B/C ball bounds use a Good point inside the ball). No gap found.
4. Constant: logs/batch1.log line 29: p=2 w=9 K=22 D=0.8530453403, so 1-D=0.1469547 < 0.147 with margin 4.5e-5 >> double-precision error (sum of 2^21 logs, rel err ~1e-12). wdim.c re-read: Gray-code and DP subset-sum counts, q_s, G cap, types=p^{K-1} all match the definition of D_p(w,K).
5. "Beats p^{-ceil(G/3)}": S_{1,3}(x)=(x+2)^3 identically (y=x+2: 1+(y-1)+(y-1)y(y+1)=y^3), so shadow bound holds at every p; D>2/3 at every p (p=2: .853, p=3: .9247, p>=5: D>=1-1/p). OK.

Minor wording issues (not refutations):
- "D := max_{w,K} D_p(w,K)" should be sup (attainment over infinitely many (w,K) not shown); harmless with the eps.
- Constants are double precision, not interval-certified (stated in the note); margin is ample.
