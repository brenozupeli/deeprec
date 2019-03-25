import os
import time
import json

from docrec.metrics.solution import accuracy
from docrec.strips.strips import Strips
from docrec.compatibility.proposed import Proposed
# from docrec.solver.solverlocal import SolverLS
from docrec.solver.solverconcorde import SolverConcorde
from docrec.pipeline import Pipeline

t0_ = time.time()
path_model = '{}/{}'.format(os.getcwd(), open('best_model.txt').read())

# reconstruction pipeline (compatibility algorithm + solver)
algorithm = Proposed(path_model, 10, (3000, 31), num_classes=2)
#solver = SolverLS(maximize=True)
solver = SolverConcorde(maximize=True, max_precision=5)
pipeline = Pipeline(algorithm, solver)

# reconstruction instances
docs1 = ['datasets/D1/mechanical/D{:03}'.format(i) for i in range(1, 62) if i != 3]
docs2 = ['datasets/D2/mechanical/D{:03}'.format(i) for i in range(1, 21)]
docs = docs1 + docs2

results = dict()
for doc in docs:
    print('Processing {} :: accuracy='.format(doc), end='')
    t0 = time.time()
    strips = Strips(path=doc, filter_blanks=True)
    solution, compatibilities, displacements = pipeline.run(strips)
    results[doc] = {
        'solution': solution,
        'compatibilities': compatibilities.tolist(),
        'displacements': displacements.tolist(),
        'time': time.time() - t0
    }
    print(accuracy(solution))

json.dump(results, open('results/results_proposed.json', 'w'))
print('Elapsed time={:.2f} sec.'.format(time.time() - t0_))
