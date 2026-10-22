# The `pairtree-cert 1` certificate format

This file specifies the certificate format completely. Paths are relative to the repository root. Someone who has not seen the generator
(`code/generator/pairtree.c`) or the checker (`code/upper/check_cert.py`) should be able to write a checker from
this file alone. §1 gives the statement a valid certificate proves, §2–§4 the syntax and the
validity conditions, §5 a reference checking algorithm, §6 the soundness proof, and §7 the
number theory that turns the statement into a bound on `r(k,2,p)`.

## 1. What a certificate proves

A certificate carries three parameters: an integer `k ≥ 2`, an integer `L ≥ 1`, and a set
`S2 ⊆ Z/k`. Write

* `P = (p_0, p_1, …, p_{M−1}) = (2, 3, 5, 7, …)` for all primes `≤ L+1`, in increasing order
  (so `M = π(L+1)` and `p_i` has index `i`, counting from 0);
* *assignment* for any map `R : P → Z/k`;
* `f_R(m) = Σ_q v_q(m)·R(q) mod k` for `1 ≤ m ≤ L+1`. Here `v_q(m)` is the exponent of `q`
  in `m`, and every prime factor of such an `m` lies in `P`.

**Statement C(k, L, S2).** For every assignment `R` with `R(2) ∈ S2` there is an integer `n`
with `1 ≤ n ≤ L` such that `f_R(n) ≡ 0` and `f_R(n+1) ≡ 0 (mod k)`.

A valid certificate (§3–§4) with no `U` lines proves C(k, L, S2) (§6).

## 2. Encoding and compression

The certificate is a byte stream of 7-bit ASCII lines. Each line ends with exactly one LF
(0x0A), including the last one. There are no CR characters, tabs, empty lines, comments,
leading or trailing spaces, or runs of two spaces.

Integers are written in decimal with no sign and no leading zeros. Zero is written `0`.

The stream may be distributed compressed with xz (`.xz`) or gzip (`.gz`). A certificate's
identity is the SHA-256 of the **decompressed** stream. The SHA-256 of a compressed file
also depends on the compressor's version and settings.

## 3. Syntax

```
pairtree-cert 1                 line 1: magic, exactly this text
k <k>                           line 2: k >= 2
L <L>                           line 3: L >= 1
R2 <v_1> <v_2> ... <v_s>        line 4: s >= 1 values, 0 <= v_1 < v_2 < ... < v_s <= k-1  (this is S2)
begin                           line 5
<node line>                     lines 6 .. : the tree, in preorder (section 4)
...
end                             the line immediately after the last node line of the tree
```

The file ends right after `end\n`. Any further byte makes the certificate invalid.

A node line is one of three forms:

| line | meaning |
|---|---|
| `B` | internal node: branch on the next prime |
| `L <n>` | leaf closed by the pair `(n, n+1)`; `n ≥ 1` |
| `U` | unresolved leaf (open case); allowed by the syntax but means "not a proof" |

## 4. Tree semantics and validity conditions

The node lines describe one rooted, ordered tree, listed in **preorder**: a node's line comes
first, then the complete listings of its children in order.

**Depth and value lists.** The root has depth 0. A child of a node at depth `d` has depth
`d+1`. For each depth `d` define the ordered value list

* `V(0) = (v_1, …, v_s)`, the `R2` list in the order given;
* `V(d) = (0, 1, 2, …, k−1)` for `d ≥ 1`.

**Internal nodes.** A `B` line at depth `d` is valid only if `d < M`, that is, only if
`p_d ≤ L+1` exists. It branches on the prime `p_d` and has exactly `|V(d)|` children. Its
`j`-th child (`j = 1, 2, …`) corresponds to `R(p_d) = V(d)_j`.

**Path assignment.** A node at depth `d` determines `R(p_0), …, R(p_{d−1})`, read off the
branch values on the path from the root. These are the assigned primes of the node.

**Leaves.** A leaf `L n` at depth `d` is valid if and only if all three of these hold:

1. `1 ≤ n ≤ L`;
2. every prime factor of `n` and of `n+1` is one of the assigned primes `p_0, …, p_{d−1}`;
3. with the path assignment, `Σ_q v_q(n)·R(q) ≡ 0 (mod k)` and
   `Σ_q v_q(n+1)·R(q) ≡ 0 (mod k)`.

Any `n` meeting these conditions is acceptable. A checker must not require `n` to be the least
such value, nor require the leaf to be at the shallowest possible depth.

**Completeness.** The stream between `begin` and `end` is exactly one such tree: the root is
the first node line. When the root's listing is complete, the next line is `end`.
Running out of lines while some `B` still lacks children is invalid. So is any node line
after the root's listing is complete.

**Verdict.** The certificate is a **proof of C(k, L, S2)** if all of the above holds and it
contains no `U` line. If everything holds but there are `U` lines, it is a well-formed
*partial* tree. The `U` leaves are exactly the open cases. Negative controls are reported
this way, never as proofs.

### Canonical form (optional; reproducibility only)

The generator writes the canonical tree for `(k, L, S2)`:

* a node at depth `d ≥ 1` is a leaf `L n` if and only if some `n ≤ L` satisfies leaf
  conditions 1–3 at that node, and then `n` is the least such value;
* otherwise the node is `B` if `d < M`, and `U` if `d = M` (every prime `≤ L+1` is assigned
  and still no pair closes);
* the root is always `B`, since no pair can satisfy condition 2 when nothing is assigned.

This tree has depth at most `M` and is uniquely determined by `(k, L, S2)`. It contains no
`U` exactly when C(k, L, S2) holds. An independent implementation of this rule should
therefore reproduce the decompressed stream byte for byte, and with it the SHA-256 in
`certificate/SHA256SUMS.decompressed`. Validity does **not** depend on canonicity.

## 5. Reference checking algorithm

```
read and validate header lines 1-5 -> k, L, S2
compute the primes p_0 < p_1 < ... < p_{M-1} <= L+1 and a factorisation method for m <= L+1
R      := array of length M
stack  := empty                         # entries [d, j]: an open B node at depth d, current child j
depth  := 0                             # depth of the node described by the next line
loop:
    line := next line                   # end of file here -> INVALID
    if line == "B":
        if depth >= M: INVALID
        push [depth, 0];  R[depth] := V(depth)[0];  depth := depth + 1
        continue
    else if line == "U":   count it
    else if line == "L n" (n canonical decimal):
        check 1 <= n <= L
        for m in (n, n+1):
            s := 0
            for each prime power q^e exactly dividing m:
                i := index of q in P;  if i >= depth: INVALID
                s := s + e * R[i]
            if s mod k != 0: INVALID
    else: INVALID
    # a leaf was just read: advance to the next sibling of the deepest unfinished B node
    while stack not empty:
        [d, j] := top of stack
        if j + 1 < |V(d)|:  top := [d, j+1];  R[d] := V(d)[j+1];  depth := d + 1;  break
        pop
    if stack is empty: break            # the root's listing is complete
next line must be "end", then end of file
VALID; it is a proof iff the number of U lines is 0
```

Some facts about this algorithm:

* A `B` at depth `d` occurs only after `p_0, …, p_{d−1}` have their path values.
* `R[i]` for `i < depth` always holds the path assignment of the node being read.
* The checker needs only a factorisation of integers up to `L+1` (a smallest-prime-factor
  sieve) and arithmetic mod `k`.
* For `k = 8, L = 1508324` the stream has 16,003,781 node lines. The bundled Python checker
  (`code/upper/check_cert.py`) needs about 40 s and 150 MB of memory on one core.

## 6. Soundness

**Claim.** If a certificate is valid with no `U` lines, then C(k, L, S2) holds.

*Proof.* Let `R` be an assignment with `R(2) ∈ S2`. Walk down from the root. At a `B` node of
depth `d`, the value `R(p_d)` occurs in `V(d)`: for `d = 0` because `R(2) ∈ S2 = V(0)`, and
for `d ≥ 1` because `V(d)` is all of `Z/k`. Go to the child with that value. Each step goes
one level deeper, and `B` nodes exist only at depths `< M`, so the walk ends at a leaf, which
must be an `L n` line. By construction the path assignment of that leaf agrees with `R` on
every assigned prime. By condition 2, `f_R(n)` and `f_R(n+1)` involve only assigned primes.
So they equal the sums in condition 3, and both are `≡ 0 (mod k)`. Condition 1 gives
`n ≤ L`. ∎

The proof uses no unit normalisation and no realisability of assignments. It also does not
use completeness or minimality of any list of "smooth pairs": the checker factors each leaf's
`n` and `n+1` itself.

## 7. From C(k, L, S2) to power residues

**Lemma 1 (index model).** Let `p` be a prime with `k | p−1`. Let `g` be a primitive root
mod `p`, and let `ind(m) ∈ Z/(p−1)` be the discrete logarithm of `m` for `p ∤ m`. Put
`R_p(q) = ind(q) mod k` for primes `q ≠ p`. Then for every integer `m ≥ 1` whose prime factors
are all `< p`, `m` is a `k`-th power residue mod `p` if and only if
`Σ_q v_q(m)·R_p(q) ≡ 0 (mod k)`.

*Proof.* `(Z/p)^*` is cyclic of order `p−1` and `ind` is an isomorphism onto `Z/(p−1)`.
Since `k | p−1`, the `k`-th powers form the subgroup `{g^{kj}}`, which is the set of
elements with `ind ≡ 0 (mod k)`. Moreover `ind(m) = Σ v_q(m)·ind(q)`. Reduce mod `k`. ∎

**Theorem.** Suppose C(k, L, S2) holds. Let `p` be a prime with `p ≡ 1 (mod k)`,
`p > L+1`, and `R_p(2) ∈ S2`. Then `r(k,2,p) ≤ L`.

*Proof.* Every prime `≤ L+1` is `< p`, so `R_p` restricted to `P` is an assignment with
`R(2) ∈ S2`. C gives `n ≤ L` with `f(n) ≡ f(n+1) ≡ 0`. Since `n+1 ≤ L+1 < p`, Lemma 1
shows that `n` and `n+1` are both `k`-th power residues. ∎

**The constraint at 2 for k = 8.** If `p ≡ 1 (mod 8)`, then `2` is a quadratic residue by the
second supplement to quadratic reciprocity (`(2/p) = 1` iff `p ≡ ±1 mod 8`). So `ind(2)` is
even, and `R_p(2) = ind(2) mod 8 ∈ {0, 2, 4, 6}`. With `S2 = {0,2,4,6}`, the `k = 8`
certificate therefore covers every prime `p ≡ 1 (mod 8)` with `p > 1508325`.

**Primes p ≢ 1 (mod 8).** Let `p` be an odd prime and `d = gcd(8, p−1) ∈ {2, 4, 8}`. In the
cyclic group `(Z/p)^*` the 8th powers and the `d`-th powers are the same subgroup, namely the
subgroup of index `d`. So `r(8,2,p) = r(d,2,p)`, as follows:

* if `p ≡ 3 or 7 (mod 8)`, then `d = 2`, and the certificate C(2, 9, Z/2) gives
  `r(8,2,p) = r(2,2,p) ≤ 9` for every prime `p > 10`;
* if `p ≡ 5 (mod 8)`, then `d = 4`, and the certificate C(4, 1224, Z/4) gives
  `r(8,2,p) = r(4,2,p) ≤ 1224` for every prime `p > 1225`. Its `S2` is all of `Z/4`, so the
  fact that 2 is a quadratic non-residue for `p ≡ 5 (mod 8)` is not needed.

Both certificates are bundled (`certificate/k2_L9.cert.xz`, `certificate/k4_L1224.cert.xz`). They give the
classical upper bounds `Λ(2,2) ≤ 9` and `Λ(4,2) ≤ 1224` (OEIS A000445 and the references
there) directly, so the argument does not rely on the literature for them.

**Corollary.** For every prime `p > 1508325`, `r(8,2,p) ≤ 1508324`. Hence
`Λ(8,2) = limsup_p r(8,2,p) ≤ 1508324`.

Primes `p ≤ L+1` are outside the statement. They are finitely many and do not affect the
limsup.
