---
title: "Consecutive eighth-power residues: $\\Lambda(8,2)=1508324$"
author: "Nathan Durfee (GitHub: AstroCat93)"
date: "Preprint, 22 October 2026. Not peer reviewed."
title-meta: "Consecutive eighth-power residues: Lambda(8,2) = 1508324"
pagetitle: "Lambda(8,2) = 1508324"
---

**Abstract.** For a prime $p$, let $r(k,2,p)$ be the least $n\ge1$ such that $n$ and $n+1$ are both nonzero $k$-th power residues modulo $p$, and let $\Lambda(k,2)=\limsup_{p\to\infty}r(k,2,p)$ (Lehmer–Lehmer). The values for $2\le k\le7$ have been known since 1964. For $k=8$, Brillhart, Lehmer and Lehmer gave the lower bound $\Lambda(8,2)\ge1200744$; Don Reble reported $1499876\le\Lambda(8,2)\le1508324$; and Fabian Arevalo published a reproducible proof of the upper bound, with a separate checker program, in 2026. We give a computer-assisted proof that $\Lambda(8,2)=1508324$. The new ingredient is the matching lower bound: an explicit exponent vector, equal to $1$ except at $74$ listed primes, whose first pair of consecutive zeros is $(1508324,1508325)$. By a theorem of Mills (1963), for every $N$, every assignment of values to the primes $q\le N$ with even value at $2$ is realised by infinitely many primes $p\equiv1\ (\mathrm{mod}\ 8)$; we include a proof for completeness. We also re-certify the upper bound with separately written programs, and note that an $18$-exception vector gives $\Lambda(9,2)\ge146290624$. The programs, the computations and the text were produced with an AI system under the author's direction; no person has verified the proofs or the code (§9).

## 1. Introduction

Lehmer and Lehmer [LL62] defined $\Lambda(k,l)=\limsup_p r(k,l,p)$ for runs of $l$ consecutive $k$-th power residues. They showed $\Lambda(2,2)=9$, and reported $\Lambda(3,2)=77$ (Dunton, published as [Du65]) and $\Lambda(4,2)=1224$ (Mills; published by Bierstedt and Mills [BM63]). Lehmer, Lehmer and Mills found $\Lambda(5,2)=7888$ and $\Lambda(6,2)=202124$ [LLM63], and Brillhart, Lehmer and Lehmer found $\Lambda(7,2)=1649375$ [BLL64, Table I]; see also [EP436]. The values for $k=5,6,7$ were proved by a machine search over "case vectors" of power characters of small primes, the method of Lehmer, Lehmer, Mills and Selfridge [LLMS62], [LLM63, §1], with the faster program of [BLL64, §3]. Section 3 uses the same method.

Each lower bound needs an infinite class of primes with prescribed power characters on the small primes. This is a theorem of Mills [Mi63, Thm 3], cited by [LLM63, §1] and [BLL64]. For $k=8$ Mills's only condition is that $R(2)$ be even. [BLL64, §8] observe that $2$ is a quadratic residue of every $p=8m+1$, so its index cannot be odd, and they use a case vector with $R(2)=2$. Rabung and Jordan [RJ70] appeal to Mills in the same way for $k=8$, with $2$ in an even class, for the different quantity $\Lambda^*(8,2)=399$. [BLL64] give only $\Lambda(8,2)\ge1200744$ (Table V), with $\Lambda(9,2)>10^7$ and $\Lambda(10,2)\ge22458303$, and no upper bound for any $k\ge8$.

Hildebrand later proved $\Lambda(k,2)<\infty$ for all $k$ [Hi91] (we rely on the summaries in [OEIS] and [EP436]). OEIS A000445 lists $9,77,1224,7888,202124,1649375$ for $k=2,\dots,7$.

In January 2020 Christopher E. Thompson added a comment to A000445: "Don Reble has reported computations proving that $1499876\le a(8)\le1508324$" [OEIS]. Reble's SeqFan post of 19 December 2019 could not be retrieved: list.seqfan.eu returned 503 and the web archive was unreachable from our environment on 15 October 2026. Its content is therefore unverified here. The one sentence of it that Hugo Pfoertner quoted in the OEIS edit history (14 January 2020) states the bounds without a method, and we found no public description of Reble's method or data. On 2 September 2026 Fabian Arevalo published a certified proof of $\Lambda(8,2)\le1508324$ [Ar], using an exhaustive case tree over the $62$ primes below $300$ and a separate checker program (Arevalo notes that the generator and the checker have the same author). The certificate file itself is not published: it is regenerated from Arevalo's code and checked against a published hash. Arevalo states $1200744\le\Lambda(8,2)\le1508324$ and leaves the exact value open. Arevalo also publishes the $108$ case vectors on the primes below $300$ that the tree leaves unsettled, and names a complete extension search on them as the route to a better lower bound [Ar, §8 and README]. Our lower bound follows that route (§4).

**Theorem 1.** $\Lambda(8,2)=1508324$. More precisely:

* **(a)** every prime $p\notin\{2,3,5,13,17,41,113\}$ has $r(8,2,p)\le1508324$, and those seven primes have no pair at all;
* **(b)** the primes $p\equiv1\ (\mathrm{mod}\ 8)$ with $r(8,2,p)=1508324$ include a set of positive Dirichlet density.

Part (a) is Reble's and Arevalo's bound, re-certified in §3. **Only (b) is new**, and with it the exact value. Within (b), the new ingredient is the vector $R^*$ of §4; realisability is Mills's theorem (Remark 5.5). The proof is computer-assisted and rests on three finite statements, (H1)–(H3).

On 15 October 2026 (last at 06:59 UTC), a search of OEIS (entry, history, pending edits), erdosproblems.com, arXiv, Crossref, GitHub and [Ar] found no earlier determination of $\Lambda(8,2)$; a partial repeat on 22 October 2026 (01:37–01:44 UTC: OEIS entry, pending edits and number search, erdosproblems.com, [Ar], GitHub code search, arXiv and Crossref) found none either. Rabung and Jordan [RJ70] treat the different quantity $\Lambda^*(k,2)$, for pairs in the same $k$-th power class, and find $\Lambda^*(8,2)=399$. Jordan (1964, doi:10.4153/CJM-1964-030-6, open access) also treats $\Lambda^*(k,m)$, for $k\le7$ only, and says nothing about $\Lambda(8,2)$. Erdős problem #436 ([ErGr80]; see [EP436]) asks three things: whether $\Lambda(k,2)$ is finite for all $k$, which Hildebrand settled; whether $\Lambda(k,3)$ is finite for all odd $k$; and how large these numbers are. Theorem 1 adds one value and does not settle the problem.

## 2. Definitions and the index model

Throughout, $p$ and $q$ are primes, $\zeta_k=e^{2\pi i/k}$, $K_k=\mathbb{Q}(\zeta_k)$, and $\pi(N)$ is the number of primes $\le N$. For a map $R$ from primes to $\mathbb{Z}/k$, put $f_R(m)=\sum_q v_q(m)R(q)$ for $m\ge1$. A *zero pair* of $R$ is an $n\ge1$ with $f_R(n)=f_R(n+1)=0$.

**Definition.** $r(k,2,p)$ is the least $n\ge1$ with $p\nmid n(n+1)$ such that $n$ and $n+1$ are $k$-th power residues mod $p$. If there is none, $r(k,2,p)=\infty$ and $p$ is *exceptional*. Then $\Lambda(k,2)=\limsup_{p\to\infty}r(k,2,p)$ [LL62], [EP436].

[LL62] admits $0$ as a residue. [LLM63] and [BLL64] take the maximum over non-exceptional $p$, [BLL64] only for $p=km+1$; [LLM63] note, via [Mi63, Thm 2], that a finite maximum is attained by infinitely many primes; the OEIS name ("latest possible occurrence … modulo any prime") is also a maximum. These conventions can differ only when $p\le n+1$, and by (H3) below they all give $1508324$ for $k=8$.

**Lemma 2.1 (index model).** Let $k\mid p-1$, let $g$ be a primitive root mod $p$, and let $R_{p,g}(q)=\mathrm{ind}_gq\bmod k$ for $q\ne p$. Then $m\ge1$ with $p\nmid m$ is a $k$-th power residue iff $f_{R_{p,g}}(m)=0$. Hence if $n_0$ is the least zero pair of $R_{p,g}$ and $p>n_0+1$, then $r(k,2,p)=n_0$.

*Proof.* The $k$-th powers in the cyclic group $\langle g\rangle$ are the $g^j$ with $k\mid j$, and $\mathrm{ind}_gm\equiv\sum_qv_q(m)\,\mathrm{ind}_gq$ mod $p-1$. $\square$

**Lemma 2.2 (reduction).** Let $p$ be odd and $d=\gcd(8,p-1)$. In $(\mathbb{Z}/p)^*$ the 8th powers and the $d$-th powers form the same subgroup, so $r(8,2,p)=r(d,2,p)$.

* **(a)** If $p\equiv3\ (\mathrm{mod}\ 4)$ and $p\ge7$, then $r(8,2,p)\le9$: one of $2,5,10$ is a quadratic residue, giving the pair $(1,2)$, $(4,5)$ or $(9,10)$ [LL62].
* **(b)** If $p\equiv5\ (\mathrm{mod}\ 8)$ and $p\notin\{5,13\}$, then $r(8,2,p)\le1224$. This is [BM63], whose exceptions are $2,3,5,13,17,41$. For $p>1225$ it also follows from the bundled $k=4$ certificate (§8).

## 3. The upper bound

Let $p_0<\dots<p_{M-1}$ be the primes $\le L+1$. Let $\mathbf{C}(L)$ be the statement that every $R:\{p_i\}\to\mathbb{Z}/8$ with $R(2)\in\{0,2,4,6\}$ has a zero pair $n\le L$.

A **case tree** is a finite rooted tree with two kinds of node. It formalises the case-vector proofs of [LLMS62], [LLM63] and [BLL64, §3].

* An internal node at depth $d<M$ branches on $p_d$. It has one child for each value in $V_0=\{0,2,4,6\}$ if $d=0$, and in $V_d=\mathbb{Z}/8$ if $d\ge1$.
* A leaf at depth $d$ is *closed* by $n\le L$ if every prime factor of $n(n+1)$ is among $p_0,\dots,p_{d-1}$ and $f(n)=f(n+1)=0$ for the path values.

**Proposition 3.1.** A case tree for $L$ with all leaves closed proves $\mathbf{C}(L)$. In turn, $\mathbf{C}(L)$ implies $r(8,2,p)\le L$ for every prime $p\equiv1\ (\mathrm{mod}\ 8)$ with $p>L+1$.

*Proof.*

* *The tree proves $\mathbf{C}(L)$.* Given $R$ with $R(2)$ even, walk down the tree choosing the child labelled $R(p_d)$, which exists because $R(p_d)\in V_d$. The walk ends at a leaf whose path agrees with $R$, and that leaf's $n$ is a zero pair of $R$.
* *$\mathbf{C}(L)$ implies the bound.* If $p\equiv1\ (\mathrm{mod}\ 8)$, then $2$ is a quadratic residue by the second supplement to quadratic reciprocity. So $\mathrm{ind}_g2$ is even and $R_{p,g}(2)\in\{0,2,4,6\}$.
* Since $p>L+1$, no $p_i$ equals $p$, and $\mathbf{C}(L)$ gives a zero pair $n\le L$ of $R_{p,g}$. As $n+1<p$, Lemma 2.1 applies. $\square$

The condition $p>L+1$ cannot be dropped: $17$, $41$ and $113$ are $\equiv1\ (\mathrm{mod}\ 8)$ and have no pair.

**(H1)** *There is a case tree for $L=1508324$ with all leaves closed.*

**The certificate.** The certificate is the preorder stream of the canonical tree, which branches on primes in increasing order, tries values in increasing order, and closes each leaf by the least admissible $n$. The stream is a header, then one line per node (`B` for a branch, `L n` for a leaf), then `end`. The tree has $2{,}000{,}473$ internal nodes and $14{,}003{,}308$ leaves, all closed. It never branches beyond $p_{60}=283$, although all $M=114765$ primes $\le1508325$ are allowed, and the leaf value $1508324$ occurs $976$ times. The stream is $101{,}385{,}765$ bytes, is regenerated in $6$ s, and has SHA-256 `f1e1c018f023acd0d57ac2705c5300bb4bf30f290d7aab4ccc1d9b306214bdf5`.

**Checks of (H1).** A standard-library Python checker written with the generator re-factors every leaf in about $40$ s. It prints the header it verified, and the reader must confirm that this reads $k=8$, $L=1508324$, $R(2)\in\{0,2,4,6\}$. Two further checkers, one in Python and one in C that factors by trial division over the assigned primes, were written in separate AI sessions from the format specification alone, without seeing the generator (§9). A canonical regenerator reproduces the stream's SHA-256, and does so for $k=2,\dots,7$ as well. A third checker takes the expected header as input, and a separately written implementation of the branching rule gives identical node counts. Both independent checkers rejected all $35$ invalid mutations of the $k=8$ stream, and on $7955$ mutants of the small certificates three checkers agreed on every verdict. For $2126$ primes $p\equiv1\ (\mathrm{mod}\ 8)$ ($2000$ random primes between $1508326$ and $10^{40}$, and all $126$ primes $p<5\cdot10^8$ with $r(8,2,p)\ge650$) we computed $R_{p,g}$ from $p$, walked the tree, and confirmed the leaf pair by modular exponentiation; there were no failures. As calibration, with all values allowed the generator closes exactly at $L=9,77,1224,7888,202124,1649375$ for $k=2,\dots,7$, and at $L-1$ it finds a full assignment with no zero pair.

**Cross-check with [Ar].** Arevalo's tree uses the $62$ primes $<300$, admitted one at a time (Arevalo's "dimension window", after the dimension $d$ of [BLL64, §2–3]), and one child per orbit of the unit stabiliser. Its soundness therefore also needs three facts: $f_{uR}=uf_R$; $\{R(2)\text{ even}\}$ is unit-invariant; and at each node the children represent every orbit of the path's stabiliser on the allowed values. Regenerated with Arevalo's `tree2.c` (commit `4404f5b`), the certificate has $3{,}999{,}920$ nodes, $3{,}499{,}913$ leaves and $0$ unsettled, as in Arevalo's log, and Arevalo's `check_tree2.py` accepts it with threshold $1508324$. Byte identity with the file Arevalo checked is unverified: our `.gz` is $20{,}970{,}409$ bytes against Arevalo's $20{,}970{,}402$ and has a different SHA-256, and Arevalo publishes no hash of the decompressed stream. At $L=1508323$, Arevalo's $108$ unsettled vectors coincide up to units with the $432$ unresolved leaves of our tree capped at depth $62$.

**(H3)** *For $3\le p\le1508325$, $r(8,2,p)=\infty$ exactly for $p\in\{3,5,13,17,41,113\}$. Otherwise $r(8,2,p)\le552$, with the maximum at $p=1476217$.* This is a direct computation with Euler's criterion; three separately written programs agree (§9).

**Theorem 3.2.** Under (H1) and (H3), $r(8,2,p)\le1508324$ for every prime $p\notin\{2,3,5,13,17,41,113\}$.

*Proof.* Use (H3) for $p\le1508325$. For larger $p$, use Lemma 2.2 if $p\not\equiv1\ (\mathrm{mod}\ 8)$, and Proposition 3.1 with (H1) if $p\equiv1\ (\mathrm{mod}\ 8)$. $\square$

## 4. The lower-bound vector

Let $R^*(q)=1$ for every prime $q$ except the following $74$:

| $R^*(q)$ | primes $q$ |
|-|---------------------------|
| $0$ | 3, 97, 149, 163 |
| $3$ | 233, 271, 443, 641, 1297 |
| $2$ | 2, 13, 29, 31, 53, 101, 113, 137, 223, 229, 241, 257, 269, 307, 311, 317, 349, 359, 479, 487, 499, 521, 557, 673, 709, 727, 821, 863, 883, 937, 1021, 1061, 1087, 1171, 1201, 1301, 1361, 1381, 1409, 1451, 1543, 1627, 1663, 2297, 2381, 2383, 2411, 3821, 4073, 4091, 4177, 4547, 5407, 5867, 6343, 6761, 8543, 10271, 15227, 16103, 24049, 24677, 26029, 32917, 33331 |

**(H2)** *For $k=8$, the least zero pair of $R^*$ is $n=1508324$.*

That $1508324$ is a zero pair can be checked by hand. We have $1508324=2^2\cdot47\cdot71\cdot113$, so $f=2\cdot2+1+1+2=8\equiv0$. We have $1508325=3\cdot5^2\cdot7\cdot13^2\cdot17$, so $f=0+2+1+2\cdot2+1=8\equiv0$.

That no smaller $n$ is a zero pair is the finite computation. C and Python programs written in separate AI sessions (§9), using a linear least-prime-factor sieve, an additive prime-power sieve and a segmented divide-out sieve, agree on it. Each takes at most a few seconds. Only primes $\le1508325$ matter; the next prime after $1508323$ is $1508383$. Resetting any listed prime other than $2$ to $1$ creates an earlier zero pair. Like the vector of [BLL64, Table V], $R^*$ has $R^*(2)=2$ and $R^*(3)=0$, and it agrees with $24$ of that vector's $39$ listed values. Restricted to the $62$ primes below $300$, $R^*$ is exactly the eleventh of the $108$ unsettled case vectors published in [Ar] (`data/gaps_k8_P300_L1500000.txt`). This must hold up to units if Arevalo's tree is correct. $R^*$ is therefore a full extension of one of those vectors, the route proposed in [Ar, §8].

$R^*$ is the greedy simplification of a full assignment of all $114765$ primes found with the SAT solver CaDiCaL, version 1.5.3 [BFF+24], called through PySAT [IMM18]. A third full assignment, found by the case-tree program run at $L=1508323$, differs from the SAT assignment at $23776$ primes and is not a unit multiple of it. All three have least zero pair $1508324$.

## 5. Realizability

For $e\in\mathbb{Z}^{\pi(N)}$, put $a_e=\prod_{q\le N}q^{e_q}$. Let $\alpha_q=q^{1/k}>0$ and $M_N=K_k(\alpha_q:q\le N)$.

**Lemma 5.1.** Let $a\in\mathbb{Q}_{>0}$ and $\alpha=a^{1/k}>0$. If $a\in(K_k^*)^k$, then $\alpha\in K_k$ and $\alpha^2\in\mathbb{Q}$.

*Proof.* If $a=y^k$ with $y\in K_k$, then $y/\alpha\in\mu_k\subset K_k$, so $\alpha\in K_k$. Then $\mathbb{Q}(\alpha)\subset\mathbb{R}$ is a subfield of the abelian field $K_k$, hence Galois over $\mathbb{Q}$. So each conjugate of $\alpha$ is a real $k$-th root of $a$, that is, $\pm\alpha$. So the minimal polynomial of $\alpha$ over $\mathbb{Q}$ is $X-\alpha$ or $(X-\alpha)(X+\alpha)=X^2-\alpha^2$, and in either case $\alpha^2\in\mathbb{Q}$. $\square$

**Corollary 5.2.**

* **(a)** $a_e\in(K_8^*)^8$ iff $4\mid e_2$ and $8\mid e_q$ for all odd $q$.
* **(b)** $a_e\in(K_9^*)^9$ iff $9\mid e_q$ for all $q$.

*Proof.* (a) For "if": since $\sqrt{2}=\zeta_8+\zeta_8^{-1}\in K_8$, we have $a_e=(\sqrt{2}^{\,e_2/4}\prod_{q\ \mathrm{odd}}q^{e_q/8})^8$. For "only if": by Lemma 5.1, $c=a_e^{1/4}\in\mathbb{Q}$, so $4\mid e_q$ for all $q$, and $\sqrt{c}\in K_8$. The quadratic subfields of $K_8$ are $\mathbb{Q}(i)$, $\mathbb{Q}(\sqrt{2})$ and $\mathbb{Q}(\sqrt{-2})$. So $c\in(\mathbb{Q}^*)^2$ or $c\in2(\mathbb{Q}^*)^2$, which is exactly the stated condition.

For (b), we have $\alpha^2\in\mathbb{Q}$ and $\alpha^9=a_e\in\mathbb{Q}$, so $\alpha=\alpha^9(\alpha^2)^{-4}\in\mathbb{Q}$. $\square$

So for $k=8$ the only extra relation is $16=(\sqrt{2})^8$. Valuations alone would also allow $4$, since $(2)=(1-\zeta_8)^4$, but $4^{1/8}=2^{1/4}\notin K_8$. For $k=9$ there is none; in particular $27$ is not a ninth power in $K_9$, as $3^{1/3}$ generates a non-normal field.

**Proposition 5.3.** Let $k\in\{8,9\}$, and define $\kappa:\mathrm{Gal}(M_N/K_k)\to(\mathbb{Z}/k)^{\pi(N)}$ by $\sigma(\alpha_q)=\zeta_k^{\kappa(\sigma)_q}\alpha_q$. Then $\kappa$ is an injective homomorphism. Its image is $\{x:x_2\text{ even}\}$ for $k=8$, and everything for $k=9$. Hence $[M_N:\mathbb{Q}]$ is $2\cdot8^{\pi(N)}$ for $k=8$ and $6\cdot9^{\pi(N)}$ for $k=9$.

*Proof.*

* *$\kappa$ is an injective homomorphism.* $\sigma\alpha_q$ is a root of $X^k-q$, and $\sigma$ fixes $\zeta_k$, so $\kappa$ is a homomorphism. It is injective because the $\alpha_q$ generate $M_N/K_k$.
* *The image lies in $\Lambda^\perp$.* Let $\Lambda=\{e:a_e\in(K_k^*)^k\}$ (a sublattice of $\mathbb{Z}^{\pi(N)}$, unrelated to $\Lambda(k,2)$), and $\Lambda^\perp=\{x\in(\mathbb{Z}/k)^{\pi(N)}:\sum_qe_qx_q=0\text{ for all }e\in\Lambda\}$. For $e\in\Lambda$, $\beta=\prod\alpha_q^{e_q}$ satisfies $\beta^k=y^k$ with $y\in K_k$. So $\beta\in K_k$ and $\sigma\beta=\beta$, that is, $\sum_qe_q\kappa(\sigma)_q=0$.
* *Counting.* By Kummer theory [MiFT, Thm 5.30], $[M_N:K_k]=(K_k^{*k}\langle q\le N\rangle:K_k^{*k})=[\mathbb{Z}^{\pi(N)}:\Lambda]$. This equals $|\Lambda^\perp|$, because $\mathbb{Z}^{\pi(N)}/\Lambda$ is finite and killed by $k$.

So $\mathrm{im}\,\kappa=\Lambda^\perp$, which Corollary 5.2 computes. $\square$

**Theorem 5.4 (realizability; Mills [Mi63, Thm 3]).** Let $k\in\{8,9\}$, $N\ge3$, and $R:\{q\le N\}\to\mathbb{Z}/k$, with $R(2)$ even if $k=8$. Let $\mathcal{P}(R)$ be the set of primes $p>N$ such that $p\equiv1\ (\mathrm{mod}\ k)$ and some primitive root $g$ has $\mathrm{ind}_gq\equiv R(q)\ (\mathrm{mod}\ k)$ for all $q\le N$.

Then $\mathcal{P}(R)$ contains every prime $p>N$ whose Frobenius class in $\mathrm{Gal}(M_N/\mathbb{Q})$ is the class $C$ of $\sigma=\kappa^{-1}(R)$. That set has Dirichlet density $|C|/[M_N:\mathbb{Q}]>0$ [MiCFT, Thm V.3.23]. It also has natural density [Le, Thm 3.1], which we do not need. In particular $\mathcal{P}(R)$ is infinite.

*Proof.*

1. *Choice of $\mathfrak P$.* $M_N$ is the splitting field of $(X^k-1)\prod_{q\le N}(X^k-q)$. Since $p\nmid k\prod q$, $p$ is unramified in $M_N$ [MiCFT, V §3]. Choose $\mathfrak P\mid p$ with $\mathrm{Frob}_{\mathfrak P}=\sigma$, so that $\sigma\beta\equiv\beta^p$ mod $\mathfrak P$.
2. *$k$ divides $p-1$.* As $\prod_{j=1}^{k-1}(1-\zeta_k^j)=k\notin\mathfrak P$, reduction mod $\mathfrak P$ is injective on $\mu_k$. As $\sigma$ fixes $\zeta_k$, we get $\zeta_k\equiv\zeta_k^p$. So $k\mid p-1$, and $\omega=\zeta_k$ mod $\mathfrak P$ is an element of $\mathbb{F}_p^*$ of order $k$.
3. *The power characters.* $\zeta_k^{R(q)}\alpha_q=\sigma\alpha_q\equiv\alpha_q^p$ and $\alpha_q\notin\mathfrak P$, so $q^{(p-1)/k}\equiv\omega^{R(q)}$.
4. *Choice of $g$.*
   * For a primitive root $g_0$, $\omega=g_0^{u(p-1)/k}$ with $u\in(\mathbb{Z}/k)^*$. Fix an integer $\tilde u$ representing $u$.
   * Write $p-1=k'm$, where every prime factor of $k'$ divides $k$ and $\gcd(m,k)=1$. Then $\gcd(\tilde u,k')=1$.
   * By the Chinese remainder theorem, choose $t\equiv\tilde u\ (\mathrm{mod}\ k')$ and $t\equiv1\ (\mathrm{mod}\ m)$. Then $g=g_0^t$ is a primitive root with $g^{(p-1)/k}=\omega$.
   * Hence $\omega^{\mathrm{ind}_gq}=q^{(p-1)/k}=\omega^{R(q)}$. $\square$

**Remark 5.5.** Replacing $g$ by $g^t$ multiplies $R_{p,g}$ by $t^{-1}$, and $f_{uR}=uf_R$, so the least zero pair depends only on $p$. Conjugation by $\tau$ with $\tau(\zeta_k)=\zeta_k^c$ multiplies $\kappa$ by $c$, so $C=\kappa^{-1}((\mathbb{Z}/k)^*R)$. For $k=8$ the parity condition is necessary, by §3. Theorem 5.4 is not new. Its infinitude statement is the case $k\in\{8,9\}$ of Mills [Mi63, Thm 3]. For $4\mid k$ Mills's condition is $\zeta_i^{k/2}=1$ whenever $4q_i\mid k$, which for $k=8$ says exactly that $R(2)$ is even; for odd $k$ there is no condition. Corollary 5.2 is the case $k\in\{8,9\}$ of Mills's Lemma on $\mathbb{Q}\cap K_k^{*k}$, our Lemma 5.1 follows Mills's proof of it, and Mills's Theorem 1 is the Chebotarev step. [BLL64, §8] and [RJ70] already use the case $k=8$. Corollary 5.2 is also consistent with Schinzel's theorem on abelian binomials [S77, Thm 2], and Schinzel remarks [S77, p. 247] that for $K=\mathbb{Q}$ and arbitrary $n$ "a more precise result has been obtained by Mills". We include a proof only to keep the note self-contained.

## 6. Proof of Theorem 1

Assume (H1)–(H3). Part (a) is Theorem 3.2.

For (b), apply Theorem 5.4 with $k=8$, $N=1508323$ (so $\pi(N)=114765$) and $R=R^*$, which has $R^*(2)=2$. The primes $\le1508325$ are exactly those $\le N$, and every $p\in\mathcal{P}(R^*)$ satisfies $p\ge1508383$. So (H2) and Lemma 2.1, applied with the primitive root of Theorem 5.4, give $r(8,2,p)=1508324$.

Since $R^*(5)=1$, $R^*$ has trivial stabiliser in $(\mathbb{Z}/8)^*$. So $|C|=4$, and $\mathcal{P}(R^*)$ contains a set of Dirichlet density $4/(2\cdot8^{114765})\approx1.5\cdot10^{-103643}$.

By (H3), the maximum over non-exceptional primes (the convention of [BLL64] and OEIS) is also $1508324$. $\square$

**Remark 6.1.** The lower bound is existential: we exhibit no realising prime. At density about $10^{-103643}$, finding one is far beyond any computation (compare [LLM63, end of §4] for $k=5,6$). Numerical tests probe only short prefixes. Among the $1.27\cdot10^7$ primes $p\equiv1\ (\mathrm{mod}\ 8)$ below $10^9$, $R_{p,g}(2)$ is never odd, and every even-$R(2)$ assignment on the primes $2,\dots,17$ occurs. [Ar, §§5, 8] expected that a larger prime set would lower $1508324$, and also proposed the extension search on the $108$ unsettled vectors that produced $R^*$. Theorem 1 shows that the extension search succeeds, so no certificate can prove a smaller bound.

## 7. A remark on $k=9$

By Corollary 5.2(b), every $R$ is admissible for $k=9$. So if $R:\{q\le N\}\to\mathbb{Z}/9$ has least zero pair $n_0$ with $n_0+1\le N$, then $\Lambda(9,2)\ge n_0$.

The vector of [BLL64, §7] has $R(3)=R(9257)=0$, and was searched only up to $10^7$. Its least zero pair is in fact $22509375=3\cdot5^5\cdot7^4$.

A better vector takes:

* $R=0$ at $3,11,173,1181,5903,9257,20773,409729$;
* $R=3$ at $769$;
* $R=2$ at $277,307,313,347,509,977,1151,1747,3631$;
* $R=1$ elsewhere.

Its least zero pair is $n_0=146290624=2^6\cdot41\cdot197\cdot283$, with $n_0+1=5^5\cdot13^2\cdot277$, as three independent programs confirm. Hence $\Lambda(9,2)\ge146290624$.

The vector came from a greedy local search that stalled, so this bound is surely not sharp. An earlier vector found in this work gave only $20000125$, below what the [BLL64] vector gives, and is not used. [RJ70] concerns $\Lambda^*$, not $\Lambda$. Jordan (1964) treats only $\Lambda^*$ for $k\le7$, and Reble's post could not be retrieved (§1), so we make no priority claim for $k=9$.

## 8. Data availability

This note is distributed in the folder `erdos-436/` of the public GitHub repository <https://github.com/AstroCat93/erdos-404-research>; paths below are relative to that folder.

* `certificate/` holds the certificates for $k=2,\dots,8$, their format specification `certificate/FORMAT.md`, and the SHA-256 sums of the compressed files and of the decompressed streams.
* `vectors/` holds $R^*$, the two full assignments of §4, the $k=9$ vector of §7, and the vector of [BLL64, Table V].
* `code/` holds the generator, all checkers, and the programs behind the other computations in this note. `code/README.md` lists, for each computational statement, the program that checks it.
* `verify.sh` checks the hashes listed below. It checks the $k=2,4,8$ certificates with four checkers and those for $k=3,5,6,7$ with two, (H3) with two programs, (H2) with five (one of them needs numpy), and the $k=9$ vector of §7 with three. It also regenerates every certificate stream with two programs. On one core it takes about 2 minutes.
* `code/extended/run_extended.sh` runs the remaining checks of §3: the separately written branching program, the tamper tests, the end-to-end test on real primes, and the negative controls. It also runs the third program for (H3), the reconstruction of $R^*$ from the SAT assignment, and the numerical test of Remark 6.1. It takes about 15 minutes.
* `code/extended/arevalo_check.sh` repeats the cross-check with [Ar] and the comparison of $R^*$ with the $108$ vectors of [Ar]. It downloads and runs Arevalo's code.

The SHA-256 hashes of the main files are:

* the $k=8$ certificate `certificate/k8_L1508324.cert.xz` (11,635,028 bytes):\
  `240670fa81675b1bb3fe387e9d9c608fbb5ca6650a5fce7649aa4a2d84c8cdcd`;
* the same, decompressed:\
  `f1e1c018f023acd0d57ac2705c5300bb4bf30f290d7aab4ccc1d9b306214bdf5`;
* the $k=2$ certificate `certificate/k2_L9.cert.xz`, decompressed:\
  `4aadaae6e1c92693ecb3a4dec9ed25603d4cb03ff4d97ffb6433b46574a27edf`;
* the $k=4$ certificate `certificate/k4_L1224.cert.xz`, decompressed:\
  `8529de46d761d830e0428ce2c982ce1f5a12c2b690bfdf04733b8bb85708b25b`;
* $R^*$ with its 74 exceptions, `vectors/vec8_compact.txt`:\
  `5f9574fbd7fe8e34e83a2d2079075c5a10fedf6aabb08eee6411c0593c9ec22b`;
* the SAT assignment of all 114765 primes, `vectors/vec8_L1508323.txt`:\
  `ec17795048a359bcedbac3529924c54adcc1b11a8197e64492c12b62546b4bc0`;
* the tree-search assignment, `vectors/k8_L1508323_witness.txt`:\
  `074cb66a0b62f6a1f354a3881accce2c7566ece89570ba7693aa97f7d26304c3`;
* the $k=9$ vector of §7, `vectors/vec9_compact18_146290624.txt`:\
  `9ad17668ee60b098968a769dbcb21551bc6c1ddd92f3c33abe0f4a5a7610573a`.

## 9. Use of AI tools; acknowledgements

The computations, the programs, the literature search and the text of this note were produced with an AI system, Claude (Anthropic), used via Claude Code, working under the author's direction. Each computational claim was re-checked in separate sessions of the same AI system, which wrote their own programs from the format specification or from the definitions without reusing the generating code. All of these sessions ran on the same underlying AI system, so their agreement is not independent in the way that checks by different people would be. Where this note calls programs independent or separately written, it means that they were written in different AI sessions. The argument of §5 was checked adversarially in a further AI session, not by a human referee. The whole note was then reviewed in further AI sessions: one for its logic and computations, one for credit to earlier work, and one before release. The corrections from all of these reviews are incorporated. Every check reported in this note was made by an AI session of the same system.

The author directed the work but has not personally verified the proofs or the code. No person has checked the arguments of this note, and no person has read the generator or the checkers line by line (compare [Ar, §7]). The author takes responsibility for the content. No AI system is an author.

The upper bound $1508324$ is due to Don Reble, who reported it together with the lower bound $1499876$. Christopher E. Thompson recorded it in OEIS A000445 with Reble's agreement, and Hugo Pfoertner preserved the relevant sentence of Reble's post in the entry's history. Fabian Arevalo gave the first public, reproducible certificate of the upper bound [Ar]. Arevalo also published the $108$ unsettled vectors and proposed the extension search that led to $R^*$. The method is that of D. H. Lehmer, Emma Lehmer, W. H. Mills, J. L. Selfridge and J. Brillhart [LLMS62], [LLM63], [BLL64], and the realisability theorem is Mills's [Mi63].

## References

Unless stated otherwise, the following were opened on 2026-10-15. Times are UTC.

* [Ar] F. Arevalo, *The first upper bound for $\Lambda(8,2)$ (Erdős #436)*, research note, 2 Sept. 2026. The README of the repository directory and its file `data/gaps_k8_P300_L1500000.txt` are cited as part of [Ar].
  * Page: https://fabianarevalo.com/power-residue-pairs (accessed 04:43Z and 05:35Z).
  * Code: https://github.com/farev/Matematica, `conjectures/power-residue-pairs`, commit 4404f5b (cloned 02:53Z).
* [BFF+24] A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks, F. Pollitt, *CaDiCaL 2.0*, Computer Aided Verification (CAV 2024), Lecture Notes in Computer Science 14681, Springer, 2024, pp. 133–152, doi:10.1007/978-3-031-65627-9_7. Cited for CaDiCaL as its authors request (README of https://github.com/arminbiere/cadical, accessed 2026-10-22 00:44Z); the version used here was 1.5.3.
* [BLL64] J. Brillhart, D. H. Lehmer, E. Lehmer, *Bounds for pairs of consecutive seventh and higher power residues*, Math. Comp. 18 (1964) 397–407, doi:10.1090/S0025-5718-1964-0164923-X.
* [BM63] R. G. Bierstedt, W. H. Mills, *On the bound for a pair of consecutive quartic residues of a prime*, Proc. Amer. Math. Soc. 14 (1963) 628–632, doi:10.1090/S0002-9939-1963-0154843-X.
* [Du65] M. Dunton, *Bounds for pairs of cubic residues*, Proc. Amer. Math. Soc. 16 (1965) 330–332, doi:10.1090/S0002-9939-1965-0172838-9.
* [EP436] T. F. Bloom, *Erdős Problem #436*, https://www.erdosproblems.com/436 (accessed 04:56Z and 06:49Z).
* [ErGr80] P. Erdős, R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, L'Enseignement Math., Geneva, 1980, p. 87 (not consulted; page as given in OEIS A000445).
* [Hi91] A. Hildebrand, *On consecutive k-th power residues. II*, Michigan Math. J. 38 (1991) 241–253, doi:10.1307/mmj/1029004331 (not consulted).
* [IMM18] A. Ignatiev, A. Morgado, J. Marques-Silva, *PySAT: A Python Toolkit for Prototyping with SAT Oracles*, Theory and Applications of Satisfiability Testing (SAT 2018), Lecture Notes in Computer Science, Springer, 2018, pp. 428–437, doi:10.1007/978-3-319-94144-8_26 (Crossref record checked 2026-10-22 00:44Z). PySAT's solver `cadical153` is CaDiCaL 1.5.3 (https://pysathq.github.io/docs/html/api/solvers.html, accessed 2026-10-22 00:44Z).
* [Le] H. W. Lenstra, *The Chebotarev density theorem*, lecture notes, https://websites.math.leidenuniv.nl/algebra/Lenstra-Chebotarev.pdf.
* [LL62] D. H. Lehmer, E. Lehmer, *On runs of residues*, Proc. Amer. Math. Soc. 13 (1962) 102–106, doi:10.1090/S0002-9939-1962-0138582-6.
* [LLM63] D. H. Lehmer, E. Lehmer, W. H. Mills, *Pairs of consecutive power residues*, Canad. J. Math. 15 (1963) 172–177, doi:10.4153/CJM-1963-020-4.
* [LLMS62] D. H. Lehmer, E. Lehmer, W. H. Mills, J. L. Selfridge, *Machine proof of a theorem on cubic residues*, Math. Comp. 16 (1962) 407–415, doi:10.1090/S0025-5718-1962-0162379-2.
* [Mi63] W. H. Mills, *Characters with preassigned values*, Canad. J. Math. 15 (1963) 169–171, doi:10.4153/CJM-1963-019-3 (PDF opened 06:56Z).
* [MiCFT] J. S. Milne, *Class Field Theory*, v4.03, https://www.jmilne.org/math/CourseNotes/CFT.pdf.
* [MiFT] J. S. Milne, *Fields and Galois Theory*, v5.10, https://www.jmilne.org/math/CourseNotes/FT.pdf.
* [OEIS] OEIS Foundation, *A000445*, https://oeis.org/A000445, revision #61 and history (accessed 04:51Z).
* [RJ70] J. R. Rabung, J. H. Jordan, *Consecutive power residues or nonresidues*, Math. Comp. 24 (1970) 737–740, doi:10.1090/S0025-5718-1970-0277469-8 (copy at https://www.cs.umd.edu/~gasarch/TOPICS/res/resRabungJordan.pdf, opened 06:55Z).
* [S77] A. Schinzel, *Abelian binomials, power residues and exponential congruences*, Acta Arith. 32 (1977) 245–274, doi:10.4064/aa-32-3-245-274.

Mentioned above but not consulted: Erdős–Graham (1980); Hildebrand (1991); Reble's SeqFan post (2019).
