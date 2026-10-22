/* rscan A B THRESH : for primes p = 1 (mod 8), A <= p < B, compute r(8,2,p) directly
 * (least n >= 1 with n^((p-1)/8) = (n+1)^((p-1)/8) = 1 mod p) and print "p r" when r >= THRESH.
 * Also prints the count of primes scanned and the maximum r seen.  p < 2^62. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __uint128_t u128;
static u64 mulm(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powm(u64 a, u64 e, u64 m) { u64 r = 1 % m; a %= m; while (e) { if (e & 1) r = mulm(r, a, m); a = mulm(a, a, m); e >>= 1; } return r; }
static int isprime(u64 n) {
    if (n < 2) return 0;
    static const u64 sp[] = {2,3,5,7,11,13,17,19,23,29,31,37};
    for (int i = 0; i < 12; i++) { if (n % sp[i] == 0) return n == sp[i]; }
    u64 d = n - 1; int s = 0; while (!(d & 1)) { d >>= 1; s++; }
    for (int i = 0; i < 12; i++) {
        u64 x = powm(sp[i], d, n);
        if (x == 1 || x == n - 1) continue;
        int ok = 0;
        for (int j = 1; j < s; j++) { x = mulm(x, x, n); if (x == n - 1) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}
int main(int argc, char **argv) {
    u64 A = strtoull(argv[1], 0, 10), B = strtoull(argv[2], 0, 10), th = strtoull(argv[3], 0, 10);
    u64 p = A + ((9 - A % 8) % 8); /* first p >= A with p = 1 mod 8 */
    u64 cnt = 0, maxr = 0, maxp = 0;
    for (; p < B; p += 8) {
        if (!isprime(p)) continue;
        cnt++;
        u64 e = (p - 1) / 8, n = 1;
        int prev = powm(1, e, p) == 1;
        for (n = 1;; n++) {
            int nx = powm(n + 1, e, p) == 1;
            if (prev && nx) break;
            prev = nx;
        }
        if (n > maxr) { maxr = n; maxp = p; }
        if (n >= th) printf("%llu %llu\n", p, n);
    }
    fprintf(stderr, "scanned %llu primes p=1 mod 8 in [%llu,%llu); max r = %llu at p = %llu\n", cnt, A, B, maxr, maxp);
    return 0;
}
