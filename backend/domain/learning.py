import numpy as np
from sklearn.cluster import OPTICS


def calculate(data):
    panel = data['panel']
    rows = sorted(data['points'], key=lambda row: row['code'])
    inputs = np.array([[row['x_cm']/55,row['y_cm']/55,row['slide']/.18] for row in rows])
    model = OPTICS(min_samples=4,min_cluster_size=4,max_eps=1.3,xi=.05,n_jobs=1)
    labels = model.fit_predict(inputs)
    independent = []
    members = {}
    noise = []
    reach = {}
    for point, label, distance in zip(rows,labels,model.reachability_,strict=True):
        code = point['code']
        reach[code]=round(float(distance),6) if np.isfinite(distance) else None
        if point['slide'] < panel['control_band']:
            independent.append(code)
        elif label == -1:
            noise.append(code)
        else:
            members.setdefault('密度组 '+str(int(label)+1),[]).append(code)
    return {'low_points':independent,'members':members,'clusters':len(members),
        'noise':len(noise)+len(independent),'other_noise':noise,'reachability':reach,
        'points_analyzed':len(rows)}
