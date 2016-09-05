import pi
from pi import invert
import tensorflow as tf
from tensorflow import float32
import numpy as np
from pi.optim import minimize_error, evaluate, gen_y, gen_loss_model
from pi.util import *

def tensor_rand(tensors):
    return {t:np.random.rand(*t.get_shape().as_list()) for t in tensors}

def gen_graph(g, batch_size, is_placeholder):
    with g.name_scope("fwd_g"):
        x = ph_or_var(float32, name="x", shape = (batch_size,1), is_placeholder=is_placeholder)
        y = ph_or_var(float32, name="y", shape = (batch_size,1), is_placeholder=is_placeholder)
        a = ((x * 2)*x - (4 * y)) + 5 + x
        b = (a + 2*a)+4
        z = a + b
        inputs = {"x":x, "y":y}
        outputs = {"z":z}

    return {"inputs":inputs, "outputs":outputs}

n_iters = 1000
batch_size = 128

# Default graph and session
g = tf.get_default_graph()
sess = tf.Session(graph=g)

in_out_var = gen_graph(g, batch_size, False)
y_batch = gen_y(g, in_out_var["outputs"])

loss, variables = gen_loss_model(in_out_var, y_batch, sess)
loss_data = evaluate(loss, in_out_var, sess, max_iterations=n_iters)

in_out_ph = gen_graph(g, batch_size, True)
x, y = in_out_ph['inputs']['x'], in_out_ph['inputs']['y']
z = in_out_ph['outputs']['z']
inv_g, inv_inputs, inv_outputs_map = pi.invert.invert((z,))

inv_outputs_map_canonical = {k:inv_outputs_map[v.name] for k,v in in_out_ph['inputs'].items()}
inv_inp_map = dict(zip(['z'], inv_inputs))
node_loss_data, std_loss_data = minimize_error(loss, inv_g, inv_inp_map, inv_outputs_map_canonical,
                                y_batch, in_out_var['inputs'], sess, max_iterations=n_iters)

# writer = tf.train.SummaryWriter('/home/zenna/repos/inverse/log', inv_g)
import numpy as np
import matplotlib.pyplot
import matplotlib.pyplot as plt
plt.plot(np.arange(n_iters), std_loss_data, 'bs', np.arange(n_iters), node_loss_data, 'g^')
plt.show()
