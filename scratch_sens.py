import os
import glob
import numpy as np

def get_critical_density(densities, probs, target_prob=0.5):
    sorted_pairs = sorted(zip(densities, probs))
    d = [pair[0] for pair in sorted_pairs]
    p = [pair[1] for pair in sorted_pairs]

    for i in range(len(p) - 1):
        if p[i] <= target_prob and p[i+1] >= target_prob:
            if p[i+1] == p[i]: return d[i]
            slope = (d[i+1] - d[i]) / (p[i+1] - p[i])
            return d[i] + slope * (target_prob - p[i])
            
    return np.nan

lambdas = [0, 0.2, 0.4, 0.6, 0.8, 1]
models = {
    1: {"name": "Strong", "data": {}},
    2: {"name": "Hub", "data": {}}
}

for mod_id in models.keys():
    for lam in lambdas:
        files = glob.glob(f"saved_run/results_sup{lam}_pop*_mod{mod_id}.npz")
        densities = []
        probs = []
        for f in files:
            pop = int(os.path.basename(f).split('_')[2].replace('pop', ''))
            density = (pop / 100.0) * np.pi * (1**2)
            data = np.load(f)
            densities.append(density)
            probs.append(data['perc_prob'])
        
        if len(densities) > 0:
            crit_d = get_critical_density(densities, probs, 0.3)
            models[mod_id]["data"][lam] = crit_d

print("Critical Densities:")
print(models)

for mod_id in models.keys():
    print(f"\nModel {mod_id} ({models[mod_id]['name']}) sensitivities:")
    data = models[mod_id]['data']
    for i in range(len(lambdas)-1):
        l1, l2 = lambdas[i], lambdas[i+1]
        if l1 in data and l2 in data:
            c1, c2 = data[l1], data[l2]
            sensitivity = (c2 - c1) / (l2 - l1)
            print(f"  lambda {l1} -> {l2}: {sensitivity:.2f}")

