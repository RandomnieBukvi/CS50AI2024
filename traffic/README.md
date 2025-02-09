# 1
idk, one conv2d and one maxpooling, with dropout. accuracy: 0.0557 - loss: 3.4951

# 2
just added one more conv2d with double kernels and maxpooling, removed the dropout. accuracy: 0.9605 - loss: 0.2264

# 3
added a dropout. accuracy: 0.9629 - loss: 0.1390. Idk why, but at the start of the training the results were worse than on second try 

# 4
decreased neurons in nn in a half. accuracy: 0.9053 - loss: 0.4233

# 5
added a new layer with 32 neurons. accuracy: 0.9261 - loss: 0.3435

# 6
one more convolution and maxpooling. accuracy: 0.9416 - loss: 0.2586


I guess, it's not likely anything to over perform the second version