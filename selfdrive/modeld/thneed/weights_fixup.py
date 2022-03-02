#!/usr/bin/env python3
import os
from common.basedir import BASEDIR
import numpy as np

from selfdrive.modeld.thneed.lib import load_thneed, save_thneed

def load_onnx_weights(fn):
  import onnx
  from onnx import numpy_helper

  model = onnx.load(fn)
  graph = model.graph
  init = {x.name:x for x in graph.initializer}

  onnx_layers = []
  for node in graph.node:
    #print(node.name)
    vals = []
    for inp in node.input:
      if inp in init:
        vals.append(numpy_helper.to_array(init[inp]))
    if len(vals) > 0:
      onnx_layers.append((node.name, vals))
  return onnx_layers

def weights_fixup():
  onnx_layers = load_onnx_weights(os.path.join(BASEDIR, "models/supercombo.onnx"))
  jdat = load_thneed(os.path.join(BASEDIR, "models/supercombo.thneed"))

  bufs = {}
  for o in jdat['objects']:
    bufs[o['id']] = o

  thneed_layers = []
  for k in jdat['kernels']:
    #print(k['name'])
    vals = []
    for a in k['args']:
      if a in bufs:
        o = bufs[a]
        if o['needs_load'] or ('buffer_id' in o and bufs[o['buffer_id']]['needs_load']):
          #print("  ", o['arg_type'])
          vals.append(o)
    if len(vals) > 0:
      thneed_layers.append((k['name'], vals))

  assert len(thneed_layers) == len(onnx_layers)

  # fix up weights

  for tl, ol in zip(thneed_layers, onnx_layers):
    print(tl[0], ol[0])
    assert len(tl[1]) == len(ol[1])
    for o, onnx_weight in zip(tl[1], ol[1]):
      # TODO: is the bias correct?
      if o['arg_type'] == "image2d_t":
        obuf = bufs[o['buffer_id']]
        saved_weights = np.frombuffer(obuf['data'], dtype=np.float16).reshape(o['height'], o['row_pitch']//2)

        if len(onnx_weight.shape) == 4:
          # convolution
          oc,ic,ch,cw = onnx_weight.shape

          if 'depthwise' in tl[0]:
            assert ic == 1
            weights = np.transpose(onnx_weight.reshape(oc//4,4,ch,cw), (0,2,3,1)).reshape(o['height'], o['width']*4)
          else:
            weights = np.transpose(onnx_weight.reshape(oc//4,4,ic//4,4,ch,cw), (0,4,2,5,1,3)).reshape(o['height'], o['width']*4)
        else:
          # fc_Wtx
          weights = onnx_weight

        new_weights = np.zeros((o['height'], o['row_pitch']//2), dtype=np.float32)
        new_weights[:, :weights.shape[1]] = weights

        err = np.mean((saved_weights.astype(np.float32) - new_weights)**2)
        fixed_err = np.mean((new_weights.astype(np.float16).astype(np.float32) - new_weights)**2)

        assert (err/fixed_err) >= 1
        print(o['size'], onnx_weight.shape, o['row_pitch'], o['width'], o['height'], "err %.2fx better" % (err/fixed_err))

        obuf['data'] = new_weights.astype(np.float16).tobytes()

  save_thneed(jdat, os.path.join(BASEDIR, "models/supercombo_fixed.thneed"))

if __name__ == "__main__":
  weights_fixup()


