# Erdős #404, round 3, track T1b: the fine structure of $K_p$ (Hensel perturbation, perfectness, Hausdorff dimension)

*Date: 2026-10-21. AI-generated (Claude), not human-refereed; the human author has not verified any mathematics. Every claim is labelled [proved], [computer-assisted], [heuristic], [conjecture] or [sketch].*

Notation follows the round-2 note (`publish-erdos404/note.md`): $v=v_p$, $\pi_j(x)=(x+1)\cdots(x+j)$, $\pi_0=1$, $S_B=1+\sum_{b\in B}\pi_b$, $g_p(x)=\sup_Bv(S_B(x))$, $K_p=\{g_p=\infty\}$, $\Phi_p$ the frozen residues of Corollary 3.3, $L_p$ the covering depth of Theorem 3.9.

## 0. Summary

1. **Regularity [proved].** For every word $e$ and every $p$, $F_e=\sum e_j\pi_j$ is, on each disc $x+p\mathbb Z_p$, a power series with $\mathbb Z_p$-coefficients (Theorem 1.2): it is locally analytic, $F_e'=\sum e_j\pi_j'$, and by Strassmann's theorem plus Theorem 3.2(a) of the note it has **finitely many zeros**, each of finite multiplicity (Theorem 1.3). This generalises Lemma 10.3 of the note to all $p$ and all $x$.
2. **Perfect kernel [proved].** Hensel's lemma for single far flips (Proposition 2.1, uniform threshold $j\ge p(2\lambda+2)$; the child is at distance exactly $p^{-(v(\pi_j(\alpha))-\lambda)}$) shows that the closure $\overline{\mathcal S}_p$ of the simple zeros is a perfect subset of $K_p$, nonempty exactly in the classes $r\notin\Phi_p$; hence $|K_p|=2^{\aleph_0}$ for every $p$ (Theorem 2.3). $-2$ is handled by an explicit family (Lemma 2.2).
3. **Accumulation at multiple zeros [proved; one case computer-assisted].** Every zero of multiplicity $k$ with $2v_p(k)+1\le p$ (and, at $p=2$, $v_2(k)\le1$) is a limit of simple zeros (Theorem 2.5, Proposition 2.6). Whether $K_p$ is perfect, and whether multiple zeros other than $-2$ exist at all, is open.
4. **Hausdorff dimension [proved + exact finite computation].** A window-code construction (Theorem 3.1, with a three-step Borel–Cantelli lemma excluding "deep traps") gives $\dim_H(K_p\cap U)\ge D_p(w,K)$ near every point of $\overline{\mathcal S}_p$, where $D_p(w,K)$ is an explicit average of $\log_p$ of the number of distinct window subset sums. In closed form $D_p\ge1-p^{-L_p}$ (Corollary 3.4; $L_p$ is the note's $e^{-1}$-covering depth, $L_2=1$). Computed: $\dim_HK_2\ge0.8530$, $\dim_HK_3\ge0.9247$, $\dim_HK_5\ge0.9691$, $\dim_HK_7\ge0.9921$, $\dim_HK_{13}\ge0.9996$ (§4). Factorial residues $d_p$ are not needed (Cauchy–Davenport already gives $p$ children per run).
5. **Box dimension and densities [proved].** $\underline\dim_BK_p\ge\dim_HK_p$, hence $\delta_G(2)\ge2^{-(0.147+o(1))G}$, improving the explicit shadow-family bound $2^{-\lceil G/3\rceil}$ (credit Kitamura). A polynomial lower bound for $\delta_G(2)$ is not proved; and contrary to the task's premise it would not by itself give $\dim_BK_2=1$, because $\delta_G$ counts approximating classes, not points of $K_2$ (§5).
6. **$p=2$ [conjecture].** $\dim_HK_2=1$ although $\mu(K_2)=0$: the window bounds increase $0.646,0.754,0.805,0.833,0.853$ for $w=1,\dots,9$, deficit $\approx0.45w^{-1/2}$ (§5).
7. **Relation (e) [proved].** $g_p(x)=-\log_p\operatorname{dist}(-1,A'_x)$, so $K_p=\{x:-1\in A'_x\}$ exactly; $x\mapsto A'_x$ is 1-Lipschitz in the Hausdorff metric (Proposition 6.1).

Nothing here decides Q1 for any natural $a$ or Q3: all constructed points of $K_p$ are limits of Hensel zeros and none is shown to be a natural number.

## 1. Analytic set-up: $F_e$ is a restricted power series on every residue disc

Throughout, $p$ is any prime, $v=v_p$, and a *word* is $e\in\{0,1\}^{\mathbb Z_{\ge0}}$ with $e_0=1$. Put
$$F_e(x)=\sum_{j\ge0}e_j\pi_j(x),\qquad \pi_j^{[i]}:=\pi_j^{(i)}/i!,\qquad M_n(x)=\max_{1\le l\le n}v(x+l).$$
By Proposition 1.2 of the note, $K_p=\bigcup_e Z(F_e)$, where $Z(F)$ is the zero set in $\mathbb Z_p$.

**Lemma 1.1 (derivative bounds) [proved].** Let $x\in\mathbb Z_p$ and $0\le i\le j$.
- (a) $\pi_j^{[i]}(x)=\sum_{I\subseteq[1,j],\,|I|=j-i}\prod_{l\in I}(x+l)\in\mathbb Z_p$.
- (b) $v(\pi_j^{[i]}(x))\ge\sum_{\ell\ge1}\max(0,\lfloor j/p^\ell\rfloor-i)\ge\lfloor j/p\rfloor-i$, uniformly in $x$.
- (c) If $x\notin\{-1,\dots,-j\}$ then $\pi_j^{[i]}(x)=\pi_j(x)\,e_i\big(\tfrac1{x+1},\dots,\tfrac1{x+j}\big)$, so $v(\pi_j^{[i]}(x))\ge v(\pi_j(x))-iM_j(x)$.

*Proof.* (a) $\pi_j(x+h)=\prod_{l=1}^j((x+l)+h)=\sum_I\prod_{l\in I}(x+l)\,h^{j-|I|}$; read off the coefficient of $h^i$. (b) Among $x+1,\dots,x+j$ at least $\lfloor j/p^\ell\rfloor$ are divisible by $p^\ell$; deleting $i$ factors leaves at least $\lfloor j/p^\ell\rfloor-i$ of them in each product of (a). Sum over $\ell$. (c) Divide (a) by $\pi_j(x)$; each $1/(x+l)$ has valuation $\ge-M_j(x)$. ∎

**Theorem 1.2 (regularity) [proved].** For every word $e$ and every $i\ge0$ the series $F_e^{[i]}(x):=\sum_je_j\pi_j^{[i]}(x)$ converges uniformly on $\mathbb Z_p$, with values in $\mathbb Z_p$, and
$$F_e(x+h)=\sum_{i\ge0}F_e^{[i]}(x)\,h^i\qquad(x\in\mathbb Z_p,\ h\in p\mathbb Z_p).$$
Hence $F_e$ is locally analytic on $\mathbb Z_p$ (in particular $C^\infty$), $F_e'=F_e^{[1]}$, and for each $x$ the function $u\mapsto F_e(x+pu)$ is a restricted power series in $\mathbb Z_p\langle u\rangle$ (coefficients $F_e^{[i]}(x)p^i\to0$).

*Proof.* By Lemma 1.1(b) the terms of $F_e^{[i]}$ have valuation $\ge\lfloor j/p\rfloor-i\to\infty$, uniformly in $x$. For $h\in p\mathbb Z_p$ the double family $\{e_j\pi_j^{[i]}(x)h^i\}_{0\le i\le j}$ has valuations $\ge\max(\lfloor j/p\rfloor-i,0)+i\ge\max(\lfloor j/p\rfloor,i)$, so only finitely many terms lie below any bound and the family is summable in any order. Summing over $i$ first gives $\sum_je_j\pi_j(x+h)=F_e(x+h)$ (finite Taylor formula); summing over $j$ first gives $\sum_iF_e^{[i]}(x)h^i$. Then $|F_e(x+h)-F_e(x)-F_e^{[1]}(x)h|\le|h|^2$, so $F_e'=F_e^{[1]}$, which is continuous. ∎

This removes the restriction $x\in\Omega$, $p=2$ of Lemma 10.3 of the note: the Taylor expansion holds at every point of $\mathbb Z_p$ for every $p$, with radius $|h|\le p^{-1}$ independent of $x$.

**Theorem 1.3 (each $F_e$ has finitely many zeros; finite multiplicity everywhere) [proved].** For every word $e$, $Z(F_e)$ is finite, and at each $x\in Z(F_e)$ there is a least $k\ge1$ (the *multiplicity*) with $F_e^{[k]}(x)\ne0$. Consequently $K_p$ is a union of uncountably many finite sets $Z(F_e)$, and $K_p=\pi_1(\mathcal Z)$ is the projection of the compact set $\mathcal Z=\{(x,e):F_e(x)=0\}\subset\mathbb Z_p\times\{0,1\}^{\mathbb N}$.

*Proof.* Fix $r\in\{0,\dots,p-1\}$ and put $\Phi(u)=F_e(r+pu)\in\mathbb Z_p\langle u\rangle$ (Theorem 1.2). If $\Phi\equiv0$, then $F_e$ vanishes on $r+p\mathbb Z_p$, which contains the negative integers $-m$, $m\equiv-r\pmod p$, $m\ge3$. But $F_e(-m)=1+\sum_{1\le j<m}e_j\pi_j(-m)=S_B(-m)$ with $B=\{j\in[1,m-1]:e_j=1\}$, and $S_B(-m)\equiv1\pmod{m-1}$ is nonzero (note, Theorem 3.2(a)). So $\Phi\ne0$, and by Strassmann's theorem (Cassels, *Local Fields*, LMS Student Texts 3, CUP 1986, Chapter 4; Koblitz, *p-adic Numbers, p-adic Analysis, and Zeta-Functions*, GTM 58, Chapter IV; theorem numbers not re-checked) a nonzero element of $\mathbb Z_p\langle u\rangle$ has finitely many zeros in $\mathbb Z_p$. For the multiplicity: if every $F_e^{[i]}(x)$ vanished, Theorem 1.2 would give $F_e\equiv0$ on $x+p\mathbb Z_p$, which we just excluded. $\mathcal Z$ is closed because $(x,e)\mapsto F_e(x)$ is continuous (uniform convergence, Lemma 1.1(b) with $i=0$). ∎

**Lemma 1.4 (Hensel for power series) [proved; standard].** Let $G(h)=\sum_{i\ge0}c_ih^i$ with $c_i\in\mathbb Z_p$ (so $G$ converges on $p\mathbb Z_p$), $\lambda:=v(c_1)<\infty$ and $V:=v(c_0)>2\lambda$. Then $G$ has exactly one zero $h^*$ with $v(h^*)>\lambda$. If $c_0\ne0$ then $v(h^*)=V-\lambda$ and $h^*\equiv-c_0/c_1\pmod{p^{2V-3\lambda}}$; always $v(G'(h^*))=\lambda$.

*Proof.* On $D=p^{V-\lambda}\mathbb Z_p\subseteq p^{\lambda+1}\mathbb Z_p$ let $T(h)=-(c_0+\sum_{i\ge2}c_ih^i)/c_1$. For $h\in D$, $v(c_ih^i)\ge2(V-\lambda)>V$ ($i\ge2$), so $T(h)\in D$ (with $v(T(h))=V-\lambda$ if $c_0\neq0$). Since $h^i-h'^i=(h-h')\sum_{a+b=i-1}h^ah'^b$, $v(T(h)-T(h'))\ge v(h-h')+(V-\lambda)-\lambda\ge v(h-h')+1$. The contraction $T$ has a unique fixed point $h^*\in D$, and $T(h)=h\iff G(h)=0$. The congruence: $h^*+c_0/c_1=-c_1^{-1}\sum_{i\ge2}c_ih^{*i}$ has valuation $\ge2(V-\lambda)-\lambda$. Derivative: $G'(h^*)=c_1+\sum_{i\ge2}ic_ih^{*\,i-1}$ and the sum has valuation $\ge V-\lambda>\lambda$. Uniqueness in $\{v(h)>\lambda\}$: if $G(h_1)=G(h_2)=0$ there, then $0=(h_1-h_2)[c_1+\sum_{i\ge2}c_i\sum_{a+b=i-1}h_1^ah_2^b]$ and the bracket has valuation exactly $\lambda$. ∎

**Lemma 1.5 (distance formula) [proved].** Let $e,\tilde e$ be words, $z\in Z(F_e)$ with $\lambda=v(F_e'(z))<\infty$, and $\tilde z\in Z(F_{\tilde e})$ with $v(\tilde z-z)>\lambda$. Put $H=F_{\tilde e}-F_e=\sum_j(\tilde e_j-e_j)\pi_j$. Then
$$v(\tilde z-z)=v(H(\tilde z))-\lambda .$$

*Proof.* $d=\tilde z-z\in p\mathbb Z_p$. By Theorem 1.2, $F_e(\tilde z)=F_e'(z)d+\sum_{i\ge2}F_e^{[i]}(z)d^i$, and the sum has valuation $\ge2v(d)>\lambda+v(d)$. So $v(F_e(\tilde z))=\lambda+v(d)$, while $F_e(\tilde z)=F_e(\tilde z)-F_{\tilde e}(\tilde z)=-H(\tilde z)$. ∎

## 2. Hensel perturbation; perfectness; accumulation

Call $x$ a *simple zero* if $F_e(x)=0\ne F_e'(x)$ for some word $e$; its *slope* (for that $e$) is $\lambda=v(F_e'(x))$. Let $\mathcal S_p$ be the set of simple zeros and $\overline{\mathcal S}_p$ its closure. For a word $e$ and a set $J\subseteq\mathbb Z_{\ge1}$ let $e^J$ be $e$ with the coordinates in $J$ flipped, and $\sigma_j=1-2e_j\in\{\pm1\}$, so $F_{e^J}=F_e+\Delta_J$ with $\Delta_J=\sum_{j\in J}\sigma_j\pi_j$.

**Proposition 2.1 (Hensel children) [proved].** Let $\alpha$ be a simple zero of $F_e$ with slope $\lambda$, and $n_0=n_0(\lambda)=p(2\lambda+2)$. For every (finite or infinite) $J\subseteq[n_0,\infty)$, $F_{e^J}$ has exactly one zero $\alpha_J$ with $v(\alpha_J-\alpha)>\lambda$. It is simple with slope $\lambda$, and $v(\alpha_J-\alpha)=v(\Delta_J(\alpha))-\lambda$ (with $\alpha_J=\alpha$ iff $\Delta_J(\alpha)=0$). In particular, if $\alpha\notin\mathbb Z_{<0}$, each single flip $j\ge n_0$ gives a simple zero $\alpha_j\ne\alpha$ with $v(\alpha_j-\alpha)=v(\pi_j(\alpha))-\lambda$ *exactly*.

*Proof.* Apply Lemma 1.4 to $G(h)=F_{e^J}(\alpha+h)$ (Theorem 1.2). Here $c_0=\Delta_J(\alpha)$ has $v\ge\min_{j\in J}\lfloor j/p\rfloor\ge2\lambda+2$, and $c_1=F_e'(\alpha)+\Delta_J'(\alpha)$ with $v(\Delta_J'(\alpha))\ge\min_{j\in J}\lfloor j/p\rfloor-1>\lambda$ (Lemma 1.1(b)), so $v(c_1)=\lambda$. For a single flip, $\pi_j(\alpha)\ne0$ because $\alpha\notin\{-1,\dots,-j\}$. ∎

So the condition "$v(\pi_j(\alpha))>2\lambda$" of the task statement is not needed in this form; $j\ge p(2\lambda+2)$ suffices uniformly in $\alpha$.

**Lemma 2.2 (simple zeros accumulating at $-2$) [proved].** For every $p$ and every $c\ge2p$, the word $e$ with $e_0=e_1=e_2=e_{c+2}=1$ (all other $e_j=0$) has a simple zero $x_c\equiv-2\pmod p$ with $v(x_c+2)=v(c!)$. Hence $-2\in\overline{\mathcal S_p\setminus\{-2\}}$.

*Proof.* With $y=x+2$: $\pi_1=y-1$, $\pi_2=(y-1)y$, $\pi_{c+2}(x)=(y-1)y\,\pi_c(y)$, so $F_e=y\,H(y)$ with $H(y)=y+(y-1)\pi_c(y)$. Then $H(0)=-c!$ and $H'(0)=1+c!-\sum_{i\le c}c!/i$. Each $c!/i=\prod_{l\le c,\,l\ne i}l$ contains at least $\lfloor c/p\rfloor-1\ge1$ multiples of $p$, so $H'(0)\equiv1\pmod p$. Lemma 1.4 (with $\lambda=0$, $V=v(c!)\ge1$) gives $y_c$ with $H(y_c)=0$, $v(y_c)=v(c!)$; then $x_c=y_c-2$ satisfies $F_e(x_c)=0$ and $F_e'(x_c)=H(y_c)+y_cH'(y_c)=y_cH'(y_c)\ne0$. ∎

**Theorem 2.3 (a perfect kernel in $K_p$) [proved].** For every prime $p$:
- (i) $\overline{\mathcal S}_p\subseteq K_p$ and $\overline{\mathcal S}_p$ is a perfect set;
- (ii) $\overline{\mathcal S}_p\cap(r+p\mathbb Z_p)\ne\emptyset$ iff $K_p\cap(r+p\mathbb Z_p)\ne\emptyset$ iff $r\notin\Phi_p$;
- (iii) hence $K_p$ contains a nonempty perfect set in every class $r\notin\Phi_p$, and $K_p$ has cardinality $2^{\aleph_0}$;
- (iv) simple zeros of words of finite support are dense in $\overline{\mathcal S}_p$.

*Proof.* (i) $K_p$ is closed (note, Theorem 3.1). A simple zero $\alpha\ne-2$ is not a negative integer ($K_p\cap\mathbb Z_{<0}=\{-2\}$, note Theorem 3.2(a)), so by Proposition 2.1 it is a limit of simple zeros $\alpha_j\ne\alpha$; $-2$ is such a limit by Lemma 2.2. Thus $\overline{\mathcal S}_p$ has no isolated points. (ii) If $r\in\Phi_p$ then $g_p\equiv0$ on the class (note, Corollary 3.3). If $r\notin\Phi_p$, Theorem 3.5 of the note gives a simple zero in the class. (iii) A nonempty perfect subset of $\mathbb Z_p$ has cardinality $2^{\aleph_0}$. (iv) If $F_e(x)=0$ with slope $\lambda$, the truncation $e|_n$ is $e^J$ with $J=\{j\ge n:e_j=1\}$; for $n\ge n_0(\lambda)$ Proposition 2.1 gives a simple zero of $F_{e|_n}$ within $p^{-(\lfloor n/p\rfloor-\lambda)}$ of $x$. ∎

*Remark (what was known).* The note already had: $K_p$ closed and nowhere dense, nonempty in every class $r\notin\Phi_p$ (Theorem 3.5), and, at $p=2$, $\mu(K_2)=0$. Uncountability and perfectness of a kernel are new here as far as we know; the proof is a direct use of Hensel's lemma plus the analyticity of Theorem 1.2.

### 2.1 Are there isolated points? Multiple zeros

By Theorem 1.3 every $x\in K_p$ is a zero of finite multiplicity $k$ of every word that vanishes at it. Lemma 10.3 of the note (non-vanishing of some Taylor coefficient) is the case $p=2$, $x\in\Omega$.

*Runs and levels.* For $x\in\mathbb Z_p\setminus\mathbb Z_{<0}$ let $l_0\ge1$ be least with $p\mid x+l_0$ and $l_i=l_0+pi$. The *run* $i$ is the set of positions $l_i,\dots,l_i+p-1$; its *level* is $L_i(x)=v(\pi_{l_i}(x))$. For $0\le r<p$,
$$\pi_{l_i+r}(x)=\pi_{l_i}(x)\,q_r,\qquad q_r=\prod_{t=1}^r(x+l_i+t)\equiv r!\pmod p,$$
so the $p$ elements of a run all have valuation $L_i$, and $L_{i+1}-L_i=v(x+l_{i+1})$. Writing $x+l_0=py$, the *jump* is $J_i:=L_{i+1}-L_i=1+v(y+i+1)$.

**Lemma 2.4 (residues of levels) [proved].** Put $f(u)=u+v(u!)=\sum_{s=1}^u(1+v(s))$.
- (a) If $p^B\mid y+i_0$ then $L_{i_0+u}-L_{i_0}=f(u)$ for $0\le u<p^B$.
- (b) For every $k\ge1$ and every $\ell\in\mathbb Z/k$ there is $B$ and $u<p^B$ with $p\mid u$ and $f(u)\equiv\ell\pmod k$.

*Proof.* (a) For $1\le s<p^B$, $v(y+i_0+s)=v(s)$. (b) Write $u=\sum_id_ip^i$ in base $p$; Legendre gives $f(u)=\sum_id_iR_{i+1}$ with $R_n=(p^n-1)/(p-1)$. Write $k=p^ak'$ with $p\nmid k'$. For $n\ge a$, $R_n\equiv R_a\pmod{p^a}$; and $R_n\bmod k'$ is purely periodic (the map $R\mapsto pR+1$ is invertible mod $k'$) with $R_1=1$, so $R_n\equiv1\pmod{k'}$ for infinitely many $n$. Hence there are infinitely many $n\ge a+2$ with $R_n\equiv\rho\pmod k$, where $\rho$ is the CRT residue $(R_a\bmod p^a,\ 1\bmod k')$, a unit mod $k$ ($R_a\equiv1\pmod p$). Take $c\equiv\ell\rho^{-1}\pmod k$, $0\le c<k$, choose $c$ such $n$ and put $d_{n-1}=1$ there, all other digits $0$. Then $d_0=0$, i.e. $p\mid u$, and $f(u)\equiv c\rho\equiv\ell$. ∎

**Theorem 2.5 (accumulation at multiple zeros) [proved].** Let $x\in K_p$ be a zero of multiplicity $k$ of some word $e$, and suppose $2v_p(k)+1\le p$. Then $x$ is a limit of simple zeros different from $x$; so $x\in\overline{\mathcal S}_p$ and $x$ is not isolated in $K_p$. In particular: every simple zero, and every zero of multiplicity prime to $p$, is an accumulation point of $K_p$; for $p=3$ also every multiplicity with $9\nmid k$; for $p\ge5$ every multiplicity with $v_p(k)\le(p-1)/2$.

*Proof.* If $x=-2$ use Lemma 2.2; so let $x\notin\mathbb Z_{<0}$. Put $w=2v(k)+1\le p$, $\kappa=v(k)$, $c_k=F_e^{[k]}(x)\ne0$, $\gamma=v(c_k)$.

*Step 1 (choice of runs).* We claim there are infinitely many runs $i^*$ such that (a) $J_{i^*}=\dots=J_{i^*+w-2}=1$, (b) $L_{i^*}\equiv\gamma\pmod k$, (c) $L_{i^*}\ge k(M+\gamma+w)+\gamma$ where $M=M_{l_{i^*}+wp}(x)$. Let $B$ be as in Lemma 2.4(b) for all residues mod $k$ simultaneously (take the max) and enlarge it so that $p^B>u+w$ for the $u$ used. An *aligned window* is a stretch of runs $i_0,\dots,i_0+p^B-1$ with $p^B\mid y+i_0$; aligned windows exist in every stretch of $p^B$ consecutive runs. In an aligned window, choose $u$ with $p\mid u$ and $f(u)\equiv\gamma-L_{i_0}\pmod k$, and set $i^*=i_0+u$: then (b) holds by Lemma 2.4(a), and (a) holds because $J_{i_0+u+t}=1+v(u+t+1)=1$ for $0\le t\le p-2$. For (c): $L_{i^*}\ge v(l_{i^*}!)$ (Lemma 1.1(b) with $i=0$), which grows linearly in $l_{i^*}$. If $M_n(x)$ is bounded, any far aligned window works. Otherwise let $l^\star_1<l^\star_2<\dots$ be the record positions of $n\mapsto M_n(x)$, with values $M^\star_1<M^\star_2<\cdots$. Since $v(l^\star_{m+1}-l^\star_m)\ge\min(v(x+l^\star_m),v(x+l^\star_{m+1}))=M^\star_m$, we have $l^\star_{m+1}-l^\star_m\ge p^{M^\star_m}$, and $M_n=M^\star_m$ on $[l^\star_m,l^\star_{m+1})$. For large $m$ this interval contains an aligned window starting beyond position $(p-1)\,[k(M^\star_m+\gamma+w)+\gamma+2\log_p(\cdot)]$ (the interval has length $\ge p^{M^\star_m}$, which beats any linear function of $M^\star_m$), and there (c) holds.

*Step 2 (the perturbation).* Fix such an $i^*$, put $V=L_{i^*}$, $s=(V-\gamma)/k\in\mathbb Z$, and let $\theta\in\mathbb Z_p^\times$ be the unit $c_kp^{ks}/p^V$. Choose subsets $R_t\subseteq\{0,\dots,p-1\}$ of the runs $i^*+t$, $0\le t<w$, so that
$$\delta:=\sum_{t<w}\sum_{r\in R_t}\sigma_{l_{i^*+t}+r}\,\pi_{l_{i^*+t}+r}(x)\equiv-\theta\,p^V\pmod{p^{V+w}} .$$
This is possible digit by digit: by (a) the run $i^*+t$ has level $V+t$, its elements are $p^{V+t}$ times units $\omega_t\sigma q_r\equiv\omega_t\sigma r!\not\equiv0\pmod p$, and by Cauchy–Davenport the subset sums of these $p$ nonzero residues cover $\mathbb Z/p$; choose $R_0,R_1,\dots$ in turn to fix the digits $V,V+1,\dots,V+w-1$. In particular $v(\delta)=V$. Let $J$ be the set of flipped positions and $e'=e^J$, so $F_{e'}=F_e+\Delta_J$ with $\Delta_J(x)=\delta$.

*Step 3 (Hensel in the rescaled variable).* Write $F_{e'}(x+h)=\sum_ia_ih^i$ with $a_0=\delta$ and $a_i=F_e^{[i]}(x)+\Delta_J^{[i]}(x)$; $F_e^{[i]}(x)=0$ for $1\le i<k$. Every $j\in J$ has $v(\pi_j(x))\ge V$ and $j\le l_{i^*}+wp$, so Lemma 1.1(c) gives $v(\Delta_J^{[i]}(x))\ge V-iM$. Put $h=p^su$ and $H(u)=p^{-V}F_{e'}(x+p^su)=\sum_ib_iu^i$, $b_i=a_ip^{is-V}$. Using (c), i.e. $s\ge M+\gamma+w$:
- $1\le i<k$: $v(b_i)\ge V-iM+is-V=i(s-M)\ge w$;
- $i=k$: $v(\Delta_J^{[k]}(x))\ge V-kM=\gamma+k(s-M)\ge\gamma+w$, so $b_k\equiv\theta\pmod{p^w}$;
- $i>k$: $v(b_i)\ge is-V=(i-k)s-\gamma\ge s-\gamma\ge w$, and $v(b_i)\to\infty$.

So $H\in\mathbb Z_p\langle u\rangle$, $H(1)\equiv-\theta+\theta\equiv0\pmod{p^w}$, and $H'(1)=kb_k+\sum_{i\ne k}ib_i$ has valuation exactly $\kappa$ (the sum has valuation $\ge w>\kappa$). Since $w>2\kappa$, Lemma 1.4 applied to $t\mapsto H(1+t)$ gives a zero $u^*$ with $v(u^*-1)\ge w-\kappa\ge1$, and $v(H'(u^*))=\kappa$. Hence $x+p^su^*$ is a zero of $F_{e'}$ at distance exactly $p^{-s}$ from $x$, with $F_{e'}'(x+p^su^*)=p^{V-s}H'(u^*)\ne0$: a simple zero. As $i^*\to\infty$, $s\to\infty$. ∎

**Proposition 2.6 ($p=2$, $v_2(k)=1$) [computer-assisted: one finite enumeration].** For $p=2$, every zero of multiplicity $k$ with $v_2(k)=1$ of any word is a limit of simple zeros.

*Proof.* Same as Theorem 2.5 with $w=3$, except Step 2. Use two consecutive runs $u,u+1$ inside an aligned window with $u\equiv2\pmod4$: then $J_u=1$ and $J_{u+1}=1+v(u+2)\ge3$, so run $u$ has level $V$, run $u+1$ level $V+1$, and every later run level $\ge V+4$. The four normalised elements mod 8 depend only on $X=x+l_u+2\bmod16$ (here $X\equiv6\pmod8$), and `code/p2k2.py` checks that for both admissible $X\bmod16$ and all $16$ sign patterns $\sigma$, the subset sums reach every odd residue mod 8 (it also shows that runs with $J_{u+1}=2$ fail for some sign patterns, which is why they are avoided). The level condition: for $u=2+\sum_{i\ge2}d_i2^i$, $f(u)=3+\sum_{i\ge2}d_iR_{i+1}$, and as in Lemma 2.4(b) the positions $n\ge3$ with $R_n\equiv1\pmod{k}$ ($R_n$ is odd, and $\equiv1\bmod k'$ periodically, $k=2k'$) let $f(u)$ take every residue mod $k$. Step 3 is unchanged ($w=3>2\kappa=2$). ∎

*What is left open.* Accumulation is not proved at zeros all of whose representing words have multiplicity $k$ with: $v_2(k)\ge2$ ($p=2$); $v_3(k)\ge2$ ($p=3$); $v_p(k)>(p-1)/2$ ($p\ge5$). The obstruction is that a $k$-th root needs $2v_p(k)+1$ controlled digits, while runs with single-digit jumps come in blocks of $p$; deeper control needs covering across gates (cf. $L_p$, §3). We do not know whether $K_p$ contains any multiple zero other than $-2$ (which is also a simple zero of $x+2$); Proposition 3.4(b) of the note excludes rational ones. **Open question: is $K_p$ perfect, i.e. $K_p=\overline{\mathcal S}_p$?** Theorem 2.5 and Proposition 2.6 show that $K_p\setminus\overline{\mathcal S}_p$ consists of points all of whose representing words have multiplicity $k$ in the excluded ranges above; in particular such $k\ge4$ for $p=2$, $k\ge9$ for $p=3$, and $k\ge p^{(p+1)/2}$ for $p\ge5$.

## 3. Hausdorff dimension: the window-code theorem

**Window data (a finite object).** Fix $w\ge1$ and $K\ge1$, and put $P=wp$. For a residue $\tau\in p\mathbb Z/p^K$ define, computing in $\mathbb Z/p^K$ (with $v(0):=K$):
$$q_s(\tau)=\prod_{t=1}^{s}(\tau+t)\ (0\le s<P),\qquad G_K(\tau)=\min\Big(K,\sum_{t=1}^{P}\min(v(\tau+t),K)\Big),$$
$$N_{w,K}(\tau)=\#\Big\{\textstyle\sum_{s\in S}q_s(\tau)\bmod p^{G_K(\tau)}:\ S\subseteq[0,P)\Big\},\qquad D_p(w,K)=\frac{p-1}{wp}\cdot\frac1{p^{K-1}}\sum_{y\bmod p^{K-1}}\log_pN_{w,K}(py).$$
$N_{w,K}(\tau)\ge p$, because $q_s\equiv s!\not\equiv0\pmod p$ for $s<p$ and, by Cauchy–Davenport, the subset sums of these $p$ nonzero residues cover $\mathbb Z/p$.

**Theorem 3.1 (window-code lower bound) [proved].** Let $p$ be prime, $w\ge1$ with $p\nmid w$, $K\ge1$. Let $\alpha$ be a simple zero of a word $e$ of finite support, $\alpha\ne-2$. Then for every $\rho>0$
$$\dim_H\big(K_p\cap B(\alpha,\rho)\big)\ \ge\ D_p(w,K).$$
By Theorem 2.3(iv) the same holds at every point of $\overline{\mathcal S}_p$, hence in every class $r\notin\Phi_p$, and also at every multiple zero covered by Theorem 2.5 / Proposition 2.6.

*Proof.* Let $\lambda$ be the slope, $l_0,l_i,L_i$ the runs and levels of §2.1 for $x=\alpha$, and fix $i_0$ so large that $l_{i_0}\ge n_0(\lambda)$, $l_{i_0}$ exceeds the support of $e$, and $P_0:=L_{i_0}(\alpha)-\lambda\ge\max(K+1,v(\alpha+2)+1)$. Window $k\ge0$ is the set of positions $a_k+[0,P)$, $a_k:=l_{i_0+kw}$ ($w$ consecutive runs). Its *type* is $\tau_k=(\alpha+a_k)\bmod p^K\in p\mathbb Z/p^K$; write $N_k=N_{w,K}(\tau_k)$, $G_k=G_K(\tau_k)$.

*Codes.* For each $k$ fix a family $\mathcal F_k$ of $N_k$ subsets of $[0,P)$ whose sums $\sum_{s\in S}q_s(\tau_k)$ are pairwise distinct mod $p^{G_k}$. For $c=(S_k)_k\in\Omega:=\prod_k\mathcal F_k$ let $J(c)=\bigcup_k(a_k+S_k)$ and let $z(c)$ be the zero $\alpha_{J(c)}$ of $F_{e^{J(c)}}$ given by Proposition 2.1 (all flipped positions lie beyond the support, so $e^{J(c)}=e+\mathbf 1_{J(c)}$). Then $z(c)\in K_p$ is simple with slope $\lambda$ and $v(z(c)-\alpha)\ge L_{i_0}(\alpha)-\lambda=P_0$, since every flipped $j$ has $v(\pi_j(\alpha))\ge L_{i_0}(\alpha)$. Consequently, for every $z=z(c)$: $z\equiv\alpha\pmod{p^{P_0}}$, so $(z+a_k)\bmod p^K=\tau_k$, $\min(v(z+n),K)=\min(v(\alpha+n),K)$ for all $n\ge1$, and $z\ne-2$, so $z\notin\mathbb Z_{<0}$ and $\mathcal L_k(z):=v(\pi_{a_k}(z))<\infty$.

*Distances.* Let $c\ne c'$ first differ in window $k$, $z=z(c)$, $z'=z(c')$. With $H=F_{e^{J(c)}}-F_{e^{J(c')}}$, Lemma 1.5 gives $v(z-z')=v(H(z))-\lambda$, and
$$H(z)=\pi_{a_k}(z)\Big[\sum_{s\in S_k}q_s^z-\sum_{s\in S'_k}q_s^z\Big]+\sum_{n\ge a_{k+1}}(\pm)\pi_n(z),\qquad q^z_s=\prod_{t\le s}(z+a_k+t)\equiv q_s(\tau_k)\pmod{p^K}.$$
The bracket has valuation $d<G_k\le K$ by the choice of $\mathcal F_k$, while the tail has valuation $\ge\mathcal L_{k+1}(z)=\mathcal L_k(z)+g_k(z)$, $g_k(z):=\sum_{t=1}^Pv(z+a_k+t)\ge G_k$. Hence
$$v(z(c)-z(c'))=\mathcal L_k(z)-\lambda+d,\qquad0\le d<G_k. \tag{3.1}$$
Put $\rho_k(z)=\mathcal L_k(z)+G_k-\lambda$. From (3.1): $c'$ agrees with $c$ in windows $0,\dots,k$ iff $v(z(c')-z(c))\ge\rho_k(z(c))$ (if the first difference is at $m\le k$, $v\le\mathcal L_m+G_m-1-\lambda\le\rho_k-1$ because $\mathcal L_m+G_m\le\mathcal L_{m+1}\le\mathcal L_k$ for $m<k$; if it is at $m>k$, $v\ge\mathcal L_{k+1}-\lambda\ge\rho_k$). In particular $c\mapsto z(c)$ is injective and continuous, $Z:=z(\Omega)\subseteq K_p\cap B(\alpha,p^{-P_0})$ is compact, and the *depth-$(k+1)$ cylinder* of $z$ is $Z\cap\bar B(z,p^{-\rho_k(z)})$. For points in different depth-$(k+1)$ cylinders these closed balls are disjoint (ultrametric balls are nested or disjoint, and nesting would put both points in one cylinder).

*Measure.* Let $\nu$ be the product of the uniform measures on the $\mathcal F_k$ and $\mu=z_*\nu$. Then $\mu(\bar B(z,p^{-\rho_k(z)}))=\nu_{k+1}:=\prod_{m\le k}N_m^{-1}\le p^{-(k+1)}$. For $p^{-\rho_{k+1}(z)}<r\le p^{-\rho_k(z)}$, $\mu(\bar B(z,r))\le\nu_{k+1}$, so
$$\liminf_{r\to0}\frac{\log\mu(\bar B(z,r))}{\log r}\ \ge\ \liminf_k\frac{\sum_{m\le k}\log_pN_m}{\rho_{k+1}(z)} .\tag{3.2}$$

*Numerator.* $\alpha+l_0=py$ and $\tau_m/p\equiv y+i_0+mw\pmod{p^{K-1}}$. As $p\nmid w$, this runs through all residues mod $p^{K-1}$ once in every $p^{K-1}$ consecutive $m$. So $\frac1k\sum_{m<k}\log_pN_m\to\frac{wp}{p-1}D_p(w,K)$.

*Denominator.* $\rho_{k+1}\le\mathcal L_{k+1}+K$ and $\mathcal L_{k+1}(z)=\mathcal L_0(z)+\sum_{a_0<n\le a_{k+1}}v(z+n)$. In an interval of $T$ consecutive integers at most $T/p^\ell+1$ have $p^\ell\mid z+n$, so the sum is $\le(k+1)P/(p-1)+\mathfrak M_{k+1}(z)$, with $\mathfrak M_k(z):=\max_{a_0<n\le a_k}v(z+n)$.

So (3.2) is $\ge D_p(w,K)$ at every $z$ with $\mathfrak M_k(z)=o(k)$. Lemma 3.2 shows this holds $\mu$-a.e.; the mass distribution principle (Lemma 3.3) then gives $\dim_HZ\ge D_p(w,K)$. ∎

**Lemma 3.2 (no deep traps) [proved].** In the setting above, $\mathfrak M_k(z)=o(k)$ for $\mu$-a.e. $z$.

*Proof.* Two facts. (F1) If $z\in Z$, $R\ge0$, and $\kappa(z,R):=\max\{m\ge0:\rho_{m-1}(z)\le R\}$ ($\rho_{-1}:=0$), then $\mu(\bar B(z,p^{-R}))\le\nu_{\kappa(z,R)}\le p^{-\kappa(z,R)}$. (F2) Among $P$ consecutive integers $n$, at most one has $v(z+n)>\beta:=\lfloor\log_pP\rfloor$; so $g_k(z)\le(P-1)\beta+\max_{n\in\text{window }k}v(z+n)$.

*Step A (exponential a-priori bound).* Let $A_k$ be the set of $z\in Z$ with $v(z+n)\ge\rho_k(z)$ for some $n$ in window $k$. Then $-n\in\bar B(z,p^{-\rho_k(z)})$; these balls are disjoint for distinct depth-$(k+1)$ cylinders, so at most $P$ cylinders meet $A_k$ and $\mu(A_k)\le P\,p^{-(k+1)}$. By Borel–Cantelli, a.e. $z$ lies in only finitely many $A_k$; for the other $k$, (F2) gives $\mathcal L_{k+1}\le2\mathcal L_k+C_0$ ($C_0=(P-1)\beta+K$), so $\mathcal L_k(z)\le C(z)2^k$.

*Step B (polynomial bound).* For $C,k_1\in\mathbb N$ let $\mathrm{Good}=\{z:\mathcal L_k(z)\le C2^k\ \forall k\ge k_1\}$ and $E_k=\{z\in\mathrm{Good}:\max_{n\in\text{window }k}v(z+n)\ge k^2\}$. If $z\in E_k$ with $v(z+n)\ge k^2$, then $\bar B(-n,p^{-k^2})=\bar B(z,p^{-k^2})$ and, by (F1) with $\rho_{m-1}\le\mathcal L_{m-1}+K\le C2^{m-1}+K$, its measure is $\le p^{-\kappa}$ with $\kappa\ge\log_2((k^2-K)/C)$ for large $k$, i.e. $\le C'k^{-2\log_2p}\le C'k^{-2}$. So $\mu(E_k)\le PC'k^{-2}$, summable. Taking the union over $C,k_1$: a.e. $z$ has $\max_{\text{window }k}v(z+n)<k^2$ eventually, hence $\mathcal L_k(z)=O(k^3)$.

*Step C.* Repeat with $\mathrm{Good}'=\{\mathcal L_k\le Ck^3\ \forall k\ge k_1\}$ and the threshold $\varepsilon k$: now $\kappa\ge((\varepsilon k-K)/C)^{1/3}-1$, so $\mu(E'_k)\le P\,p^{-c(\varepsilon k)^{1/3}}$ is summable. Hence a.e. $z$ has $\max_{\text{window }k}v(z+n)<\varepsilon k$ for large $k$, i.e. $\mathfrak M_k\le\varepsilon k+O_z(1)$. Intersect over $\varepsilon=1/j$. ∎

**Lemma 3.3 (mass distribution principle, local form) [proved; standard].** Let $\mu$ be a finite Borel measure on a compact $Z\subseteq\mathbb Z_p$ with $\liminf_{r\to0}\log\mu(\bar B(z,r))/\log r\ge s_0$ for $\mu$-a.e. $z$, $\mu(Z)>0$. Then $\dim_HZ\ge s_0$.

*Proof.* Let $s<s_0$. For a.e. $z$ there is $r_0(z)>0$ (taken from a countable set of radii, so $r_0$ is measurable) with $\mu(\bar B(z,r))\le r^s$ for $r<r_0(z)$. Pick $\eta>0$ with $\mu(F)>0$, $F=\{r_0\ge\eta\}$. Points of $F$ are $\mu$-null. Given a cover of $F$ by sets $U_i$ of diameter $<\eta$ meeting $F$ at $z_i$, ultrametricity gives $U_i\subseteq\bar B(z_i,\operatorname{diam}U_i)$, so $\mu(F)\le\sum_i\mu(\bar B(z_i,\operatorname{diam}U_i))\le\sum_i(\operatorname{diam}U_i)^s$ (sets of diameter $0$ are single points, of measure $0$). Thus $\mathcal H^s(F)\ge\mu(F)>0$. ∎

(For background, the local mass distribution principle is e.g. Falconer, *Techniques in Fractal Geometry*, Wiley 1997, Prop. 2.3; we did not re-check that numbering, and the proof above is self-contained.)

**Corollary 3.4 (closed-form bounds) [proved].** Let $E'_p=\{\prod_{t=1}^s(t-p):0\le s<p\}$ and $L_p=\max\{L:$ the subset sums of $E'_p$ cover $\mathbb Z/p^L\}$. For odd $p$, $E'_p=(p-1)!\,E_p$, so $L_p$ is the quantity of the note's Theorem 3.9; for $p=2$, $E'_2=\{1,-1\}$ and $L_2=1$. Then for every $p$ and every $\alpha$ as in Theorem 3.1,
$$\dim_H(K_p\cap B(\alpha,\rho))\ \ge\ D_p(1,L_p+1)\ \ge\ 1-p^{-L_p}.$$
Numerically: $\ge1/2$ ($p=2$), $2/3$ ($3$), $4/5$ ($5$), $48/49$ ($7$), $120/121$ ($11$), $168/169$ ($13$), $1-p^{-3}$ ($17,19$), $1-23^{-4}$, $1-p^{-5}$ ($29,31$), and $1-p^{-6}$, $1-p^{-5}$ for $37\le p\le53$, $59\le p\le97$ (using the note's lower bounds for $L_p$).

*Proof.* For $w=1$, $P=p$ and the only $t\le p$ with $p\mid\tau+t$ is $t=p$, so $G_K(\tau)=\min(K,v(\tau+p))=:J$. Modulo $p^J$, $\tau\equiv-p$, so $q_s(\tau)\equiv\prod_{t\le s}(t-p)$, and $N_{1,K}(\tau)\ge p^{\min(J,L_p)}$. With $y$ uniform mod $p^{K-1}$ and $K\ge L_p+1$, $J=1+v(y+1)$ and $\mathbb E\min(J,L_p)=\sum_{s=0}^{L_p-1}p^{-s}=(1-p^{-L_p})\frac p{p-1}$. ∎

*Remark (single flips and factorial residues).* Using only $S=\emptyset$ and single flips $S=\{s\}$ in each run gives $N\ge1+d_p$, $d_p=\#\{r!\bmod p:0\le r<p\}$, and the bound $\frac{p-1}p\log_p(1+d_p)$, which is the shape suggested in the task. Since Cauchy–Davenport already gives $N\ge p$, $d_p$ plays no role in Theorem 3.1. For the record, $d_2=1,d_3=2,d_5=3,d_7=4,d_{11}=5,d_{13}=9$ (computed directly); the elementary bound $d_p\ge\sqrt{p-1}$ holds because every $r\in[1,p-1]$ is a ratio $r!/(r-1)!$ of two elements of the residue set. The literature on $\#\{r!\bmod p\}$ (Cobeli–Vâjâitu–Zaharescu 2000; Garaev–Luca–Shparlinski 2004/05; Klurman–Munsch 2017, all as verified by the round-3 literature gate) is therefore not needed.

*Remark (why not dimension 1).* The loss in Corollary 3.4 comes only from runs followed by a gate of depth $J>L_p$, where only $L_p$ of the $J$ new digits are controlled. Windows of $w>1$ runs (Theorem 3.1) recover part of this loss; §4 computes $D_p(w,K)$ exactly. If for every $T$ there were window lengths covering every gate of depth $\le T$ (this is the $\mathrm{UC}(p)$ hypothesis of the note, Theorem 3.12), the same argument would give $\dim_HK_p=1$ near every simple zero [sketch: we have not written out the bookkeeping for windows that are not unions of runs].

## 4. Computations of the dimension bounds

All values are $D_p(w,K)$ of Theorem 3.1, computed exactly (integer counts) by `code/wdim.c`, rounded **down** at the 4th decimal; timings are on one core (log `logs/batch1.log`). Five cases were reproduced to 10 digits by the independent brute force `code/wdim_check.py`. The $p=2$, $w\ge7$ runs were preceded by registered predictions (`PREDICTIONS_registered_T1b.txt`, 2026-10-21T22:18:27Z), all four of which were confirmed.

| $p$ | $(w,K)$: $D_p(w,K)$ | best rigorous lower bound for $\dim_H(K_p\cap U)$ | $1-p^{-L_p}$ (Cor. 3.4) |
|---|---|---|---|
| 2 | (1,2): .6462; (3,16): .7543; (5,16): .8054; (7,20): .8330; (7,22): .8333; (9,20): .8464; (9,22): **.8530** (801 s) | **0.8530** | 0.5 |
| 3 | (1,8): .8068; (2,10): .8591; (4,12): .9111; (5,13): **.9247** (18 s) | **0.9247** | 0.6667 |
| 5 | (1,7): .9236; (2,8): .9548; (3,8): **.9691** | **0.9691** | 0.8 |
| 7 | (1,5): .9855; (2,6): **.9921** | **0.9921** | 0.9796 |
| 11 | (1,5): **.9982** | **0.9982** | 0.9917 |
| 13 | (1,5): **.9996**; (2,4): .9993 ($K$ too small) | **0.9996** | 0.9940 |
| 17, 19, 23 | (1,4): .99996, .99999, .99999 | as listed | $1-p^{-3},1-p^{-3},1-p^{-4}$ |

$U$ is any neighbourhood of any point of $\overline{\mathcal S}_p$ (in particular $K_p\cap(r+p\mathbb Z_p)$ for every $r\notin\Phi_p$ has at least this dimension). The $p=2$ value increases with $K$ at fixed $w$ (capping $G$ at $K$ loses digits at deep gates), so $(9,22)$ is not the limit for $w=9$. Deficits $1-D_2$: $.354,.246,.195,.167,.147$ for $w=1,3,5,7,9$ (largest $K$), consistent with $\approx0.45\,w^{-1/2}$ [heuristic fit].

## 5. Box dimension, densities, and $p=2$

**Proposition 5.1 (box dimension) [proved / computer-assisted].** For every $p$, $1\ge\overline{\dim}_BK_p\ge\underline{\dim}_BK_p\ge\dim_HK_p\ge\max_{w,K}D_p(w,K)$, with the values of §4. In particular $\dim_BK_p$ (if it exists) is $\ge1-p^{-L_p}$, and for $p=2$ it is $\ge0.8530$ (from $D_2(9,22)$).

*Proof.* $\dim_H\le\underline{\dim}_B$ always; the rest is Theorem 3.1. ∎

**The census does not determine $\dim_BK_2$.** Let $N_G(K_p)$ be the number of classes mod $p^G$ that meet $K_p$, and $\delta_G=\mu\{g_p\ge G\}$. Then $N_G(K_p)\le p^G\delta_G$, and $K_p\cap c\ne\emptyset$ iff the class $c$ contains a surviving class at *every* deeper level (compactness: a limit of points $x_G\in c$ with $g_p(x_G)\ge G$ lies in $K_p$, since $g_p(x)\ge\min(g_p(x_G),v(x-x_G))$). Since $\delta_G(2)\to0$ (Theorem 10.1 of the note), a polynomial *lower* bound on $\delta_G(2)$ would give $\lim\log(p^G\delta_G)/(G\log p)=1$ for the approximating sets $\{g_2\ge G\}$, but not for $K_2$ itself: a class can survive to level $G$ and die later. So the task's suggestion "dim$_B K_2=1$ follows from a polynomial lower bound on $\delta_G(2)$" is **not** correct as stated; the implication goes the other way:

**Corollary 5.2 (exponential lower bound for $\delta_G$) [proved / computer-assisted].** For every $p$ and every $\varepsilon>0$, $\delta_G(p)\ge p^{-(1-D+\varepsilon)G}$ for all large $G$, where $D=\max_{w,K}D_p(w,K)$. For $p=2$: $\delta_G(2)\ge2^{-(0.147+\varepsilon)G}$ for large $G$.

*Proof.* $\underline{\dim}_BK_p\ge D$ gives $N_G(K_p)\ge p^{(D-\varepsilon)G}$ for large $G$, and every class meeting $K_p$ lies in $\{g_p\ge G\}$ (locality, note Theorem 3.1(a)). ∎

*Explicit classes (credit: Kitamura's shadow family).* The cube identity $S_{\{1,3\}}=(x+2)^3$ gives $\{g_p\ge G\}\supseteq-2+p^{\lceil G/3\rceil}\mathbb Z_p$, hence the explicit bound $\delta_G(p)\ge p^{-\lceil G/3\rceil}$; at $p=2$ this is the class of Kitamura's shadow family $a=2^t-2$ (`KitaKen1/erdos-404-p2-landscape`, `witness_gallery.md` §7). More generally, a simple zero $\alpha$ of slope $\lambda$ of a *finite* word $T$ gives $\{g_p\ge G\}\supseteq\alpha+p^{G-\lambda}\mathbb Z_p$ (for $G>2\lambda$: $v(S_T(x))=\lambda+v(x-\alpha)$). Corollary 5.2 beats the shadow bound as soon as $1-D<1/3$, which holds for every $p$ ($1-D<0.2$ already at $p=3$, $w=1$; $0.147$ at $p=2$). A *polynomial* lower bound for $\delta_G(2)$ (Monte Carlo: $\delta_G(2)\approx5.5/G$, track T4) remains **open**: it is a statement about the approximating sets, which the Hensel tree, built from points of $K_p$, cannot see.

**Proposition 5.3 ($\dim_HK_2$) [computer-assisted lower bounds; conjecture for the value].** $\dim_HK_2\ge D_2(w,K)$ for every odd $w$; the values increase with $w$ (§4). The window bound is a *branching lower bound*: $\log_2N_{w,K}(\tau)$ is the number of bits of distinct targets that the $2w$ elements of a window can produce at the levels it gains, i.e. the log of the number of distinct alive descendants modulo the gained precision, averaged over the environment $\tau$; it is exactly the "multiplicity of alive paths" in the sense of the task, measured per window rather than per class. The deficit $1-D_2(w)$ fell from $0.354$ ($w=1$) to $0.246,0.195,0.167,0.147$ ($w=3,5,7,9$), roughly like $0.45\,w^{-1/2}$ (or like $0.6\log w/w$; the data cannot distinguish).

**Conjecture 5.4.** $\dim_HK_2=1$ (while $\mu(K_2)=0$), and $\lim_{w\to\infty}\sup_KD_2(w,K)=1$. *Heuristic:* $p=2$ is exactly critical; for a window of $2w$ elements and $G\approx2w$ gained levels, the number of subsets hitting a given residue is a critical branching count, which is positive with probability $\gtrsim1/\mathrm{poly}(w)$; then $\log_2N\approx G-O(\log w)$. A proof would need, for the fixed-$\tau$ subset sums of a window, a lower bound $\mathbb E_\tau\log_2N_w(\tau)\ge2w-o(w)$; the annealed collision count $\mathbb E_\tau\sum_rm_\tau(r)^2$ cannot give it (rare shadow types $\tau\approx-2$ dominate it, as in track T4), so a quenched argument is required.

**Conjecture 5.5 (odd $p$).** $\dim_HK_p=1$ for every odd $p$; this already follows from $\mu(K_p)>0$ (Conjecture 5.2 of the note), and also from $\mathrm{UC}(p)$ by the Remark after Corollary 3.4 [sketch]. Unconditionally we have $\ge D_p$ of §4 (e.g. $\ge0.9996$ at $p=13$).

## 6. The relation $K_p=\{x:-1\in A'_x\}$ and $g_p=-\log_p\operatorname{dist}(-1,A'_x)$

Let $A'_x=\{\sum_{j\ge1}e_j\pi_j(x):e\in\{0,1\}^{\mathbb Z_{\ge1}}\}$ (so $A_x=A'_x\cup(1+A'_x)$ in the notation of the note's §1.5).

**Proposition 6.1 [proved].**
- (a) $A'_x$ is compact, and the finite sums $\{S_B(x)-1\}$ are dense in it.
- (b) $g_p(x)=-\log_p\operatorname{dist}(-1,A'_x)$ (with $-\log_p0=\infty$); in particular $K_p=\{x\in\mathbb Z_p:-1\in A'_x\}$ exactly.
- (c) $d_H(A'_x,A'_y)\le|x-y|_p$ (Hausdorff distance); hence $g_p(x)\ge\min(g_p(y),v(x-y))$, which is the note's locality Theorem 3.1(a), and $x\mapsto A'_x$ is 1-Lipschitz.
- (d) (local structure near a simple zero) If $F_e(\alpha)=0$ with slope $\lambda$, $e$ supported in $[0,n]$, $n\ge n_0(\lambda)$, then $K_p\cap\bar B(\alpha,p^{-(\lambda+1)})\supseteq\{\alpha_J:J\subseteq(n,\infty)\}$ and, by Lemma 1.5, $|\alpha_J-\alpha_{J'}|=p^{\lambda}\,|\Delta_J(\alpha_J)-\Delta_{J'}(\alpha_J)|$: to first order the local piece of $K_p$ is the image of the tail achievement set $\{\Delta_J(\alpha)\}=A'_{>n}(\alpha)$ under $t\mapsto\alpha-t/F_e'(\alpha)$, but with the tail evaluated at the moving point.

*Proof.* (a) $e\mapsto\sum e_j\pi_j(x)$ is continuous on the compact space $\{0,1\}^{\mathbb N}$ (terms have valuation $\ge\lfloor j/p\rfloor$); truncations are dense. (b) $v(1+S)\ge G$ for some finite $S$ iff $\operatorname{dist}(-1,\text{finite sums})\le p^{-G}$ iff (by density) $\operatorname{dist}(-1,A'_x)\le p^{-G}$; and $-1\in A'_x$ is Proposition 1.2 of the note. (c) $\pi_j(x)-\pi_j(y)\in(x-y)\mathbb Z_p$ termwise, so the same word moves each point by at most $|x-y|$. (d) Proposition 2.1 and Lemma 1.5. ∎

So the structure of $K_p$ near a simple zero is governed by the *tail achievement sets* $A'_{>n}(x)$; Theorem 3.1 is a quantitative version of (d), and fullness of a tail ($A'_{>n}(x)\supseteq p^{V}\mathbb Z_p$ locally uniformly) would give $\dim=1$ and positive measure there. For $p=2$ no $A_x$ is full (note, Theorem 3.8), consistent with $\mu(K_2)=0$.

## 7. Gaps, open questions, credit, reproduction

**Status of the deliverables.**
- (a) [proved] $\overline{\mathcal S}_p\subseteq K_p$ is perfect and meets every class $r\notin\Phi_p$; $K_p$ has the cardinality of the continuum; every $F_e$ is locally analytic with finitely many zeros, so every point of $K_p$ has finite multiplicity for every representing word. Accumulation is proved at every simple zero and at zeros of multiplicity $k$ with $2v_p(k)+1\le p$ (plus $v_2(k)=1$ at $p=2$, computer-assisted finite check). **Open:** whether $K_p$ is perfect; whether multiple zeros other than $-2$ exist.
- (b) [proved + exact finite computation] $\dim_H(K_p\cap U)\ge D_p(w,K)\ge1-p^{-L_p}$ near every point of $\overline{\mathcal S}_p$.
- (c) [proved] $\underline{\dim}_BK_p\ge\dim_HK_p$; exponential lower bounds for $\delta_G(p)$ (Corollary 5.2). A polynomial lower bound for $\delta_G(2)$ is **not** proved and would not by itself determine $\dim_BK_2$ (§5).
- (d) [conjecture] $\dim_HK_2=1$, supported by the monotone sequence $D_2(w)$; no proof.
- (e) [proved] $K_p=\{x:-1\in A'_x\}$ and $g_p(x)=-\log_p\operatorname{dist}(-1,A'_x)$ (Proposition 6.1).

**Gaps and caveats.**
1. All proofs are AI-written and AI-checked only (no human referee). The longest argument is Lemma 3.2 (three Borel–Cantelli bootstraps); its weakest point is bookkeeping, not ideas.
2. The values $D_p(w,K)$ are exact integer counts $N_{w,K}(\tau)$ (C program `wdim.c`, cross-checked against the independent Python brute force `wdim_check.py` in 7 cases with identical output to 10 digits), combined in double precision; the reported decimals are rounded down. They are therefore rigorous lower bounds up to floating-point rounding of a sum of logarithms (relative error $<10^{-12}$), not interval-certified.
3. Corollary 3.4 for $37\le p\le97$ uses the note's archived lower bounds on $L_p$, which this track did not re-run.
4. `hensel_check.py` is a sanity check of Proposition 2.1, Lemma 2.2 and formula (3.1) in exact arithmetic mod $p^{60}$–$p^{80}$ (all checks passed; output `data/hensel_check.out`); it is not part of any proof.
5. Proposition 2.6 relies on a 64-configuration enumeration (`p2k2.py`); the reduction of the mod-8 question to $X\bmod16$ is argued in the text.
6. The heuristic rates in Proposition 5.3/Conjecture 5.4 are fits to four or five numbers.
7. Theorem 3.1 requires $p\nmid w$ (so that window types equidistribute); windows with $p\mid w$ would need a minimum over cosets.

**Credit.** The normal form, $K_p$, Theorems 3.1–3.5 and 3.8–3.9 and Proposition 3.4 used here are from the round-1/2 note, which credits Kovač, Tao, Lin and Kitamura as described there. The explicit classes $-2+p^{\lceil G/3\rceil}\mathbb Z_p$ are Kitamura's cube identity / shadow family (`KitaKen1/erdos-404-p2-landscape`). Hensel's lemma, Strassmann's theorem, Cauchy–Davenport and the mass distribution principle are classical. *Novelty search (2026-10-21, web search, two queries):* no work on Hausdorff dimension of $K_p$, of zero sets of factorial-type $p$-adic series, or of $p$-adic achievement sets was found; related but different: Abram–Lagarias, $p$-adic path set fractals (arXiv:1210.2478; dimension formulas for automaton-defined subsets of $\mathbb Z_p$), real achievement sets (Bartoszewicz–Głąb–Marchwicki; arXiv:2509.20181 on signed null sequences and Hausdorff dimension). The search was limited and is not exhaustive.

**Reproduction** (work dir `e404r3/T1b-Kp-structure`; 1 core):
- `clang -O2 -o code/wdim code/wdim.c -lm`; `./code/wdim p w K` (batch: `code/run_batch.sh`, log `logs/batch1.log`, timings inside).
- `python3 code/wdim_check.py 2,3,7 3,2,5 5,1,4 2,5,6 7,1,3` (independent brute force; identical values).
- `python3 code/hensel_check.py > data/hensel_check.out` (0.1 s).
- `python3 code/p2k2.py > data/p2k2.out`.
- Registered predictions: `PREDICTIONS_registered_T1b.txt` (written before the $w\ge7$ runs).
