from reverseflow.compare import compare
import sys
import getopt
import tensorflow as tf
import numpy as np
from reverseflow.util import *


## Constant
def constant_fwd_f(inputs):
    x, y = inputs['x'], inputs['y']
    a = (x*y)
    z = a * 2 + x
    outputs = {"z": z}
    return outputs

def constant_gen_graph(g, batch_size, is_placeholder):
    with g.name_scope("fwd_g"):
        x = ph_or_var(tf.float32, name="x", shape=(batch_size, 128),
                      is_placeholder=is_placeholder)
        y = ph_or_var(tf.float32, name="y", shape=(batch_size, 128),
                      is_placeholder=is_placeholder)
        inputs = {"x": x, "y": y}
        outputs = constant_fwd_f(inputs)
        return {"inputs": inputs, "outputs": outputs}


def main(argv):
    options = {'batch_size': 512, 'max_time': 100.0,
               'logdir': '/home/zenna/repos/inverse/log',
               'template': template_dict,
               'nnet_enhanced_pi': False,
               'pointwise_pi': False,
               'min_fx_y': False,
               'nnet': True,
               'min_fx_param': False,
               'rightinv_pi_fx': True,
               'nruns': 2}
    gen_graph = constant_gen_graph
    fwd_f = constant_fwd_f
    min_param_size = 1
    param_types = {'theta': tensor_type(dtype=tf.float32,
                   shape=(options['batch_size'], min_param_size),
                   name="shrunk_param")}

    param_gen = {k: infinite_samples(np.random.rand, v['shape'])
                  for k, v in param_types.items()}
    shrunk_param_gen = dictionary_gen(param_gen)
    return compare(gen_graph, constant_fwd_f, param_types, shrunk_param_gen, options)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    global runs
    runs = main(sys.argv)
    import pi
    rf.analysis.plot(runs, 30.0)
