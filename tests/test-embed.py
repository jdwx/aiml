

import numpy as np
import pickle
import sys


from tensorflow.keras.layers import Embedding
from lib.Config import config_from_tag


config = config_from_tag( sys.argv[ 1 ] )

print( "Loading pre-trained embed weights..." )
with open( config[ 'embed_weights' ], 'rb' ) as f:
    embed_weights = pickle.load( f )

vocab_size = embed_weights.shape[ 0 ]
embed_dims = embed_weights.shape[ 1 ]
input_length = 1

embed = Embedding( vocab_size, embed_dims, input_length = input_length, weights = [ embed_weights ], trainable = False )

key = 131
x = np.array( key )
y = embed( x ).numpy()
print( y[ 0 : 5 ] )
print( embed_weights[ key ][ 0 : 5 ] )
z = y - embed_weights[ key ]
print( z[ 0 : 5 ] )
print( "max diff =", z.max() )
