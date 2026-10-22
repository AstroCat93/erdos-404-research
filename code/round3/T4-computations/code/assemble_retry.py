# results_retry.json = results.json (first-attempt assembler, re-run on complete data) + retry additions
import json, os, csv
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R=json.load(open(W+"/data/results.json")); R["generated"]="2026-10-12 (runs) / 2026-10-20 (retry: verification, post-processing, deep lifts)"
def tsv(fn): return list(csv.DictReader(open(W+fn),delimiter="\t"))
R["annealed_overview"]=tsv("/data/annealed_overview.tsv"); R["annealed_buckets"]=tsv("/data/annealed_buckets.tsv")
R["kitamura_11p5_comparison"]=tsv("/data/kitamura_11p5_comparison.tsv")
R["xcheck_annealed_independent_program"]=json.load(open(W+"/data/xcheck_annealed.json"))
deep=[]
for l in open(W+"/data/deep_lift.txt"):
    if l[0]=="#": continue
    f=l.split(); deep.append({"a":int(f[0]),"g_capped":int(f[1]),"maxpop":int(f[2]),"steps":int(f[3]),"cpu_s":float(f[4])})
R["deep_lift_p2add"]={"note":"g_capped == CAP means g_2(a) >= CAP; caps: 3456/4900, 1102/11600, 34/18500, 2210/16382, 594/16382","rows":deep,
  "new_exact_value":{"a":2210,"g_2":6261,"v_2(2210!)":2206,"f(2210,2)":8467},
  "kitamura_records_reproduced":{"34":18412,"1102":11536,"3456":4823}}
R["gate_integral_node_checks"]={"p13_ngl8":"0.00330918392125","p13_ngl12":"0.00330918392005","p11_ngl16":"0.00816212220575","p11_ngl32":"0.00816212220551"}
R["mc_fits"]={"all_G>=64":"delta ~ 1.921 G^-0.813","G>=128":"2.803 G^-0.886","G>=256":"3.568 G^-0.930","local_exponents":{"64-96":0.688,"96-128":0.880,"128-192":0.825,"192-256":0.951,"256-384":0.899,"384-512":1.003,"512-768":0.846,"768-1024":1.038,"1024-1536":1.029,"1536-2046":1.156}}
json.dump(R,open(W+"/data/results_retry.json","w"),indent=1); print("keys:",list(R))
