import numpy as np
from nessi.globopt import Swarm


def test_init_pspace_one_line():
    """
    swarm.init_pspace test for one point search.
    """
    pspace_output = np.zeros((1, 2, 3), dtype=np.float32)
    pspace_output[0,0,0] = -3.0
    pspace_output[0,0,1] = 3.0
    pspace_output[0,0,2] = 0.6
    pspace_output[0,1,0] = -3.0
    pspace_output[0,1,1] = 3.0
    pspace_output[0,1,2] = 0.6
    swarm = Swarm()
    swarm.init_pspace('data/pspace_one_line.txt')
    np.testing.assert_equal(swarm.pspace, pspace_output)

def test_init_pspace_multi_line():
    """
    swarm.init_pspace test for multipoints search.
    """
    pspace_output = np.zeros((3, 2, 3), dtype=np.float32)
    pspace_output = np.array([
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]],
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]],
        [[-3.0, 3.0, 0.6],
         [-3.0, 3.0, 0.6]]
        ], dtype=np.float32)
    swarm = Swarm()
    swarm.init_pspace('data/pspace_multi_line.txt')
    np.testing.assert_equal(swarm.pspace, pspace_output)

def test_init_particles():
    """
    swarm.init_particles test.
    """
    output = np.array([[[-0.49786797,  1.321947  ],
                        [-2.9993138 , -1.1860045 ],
                        [-2.1194646 , -2.4459684 ]],
                       [[-1.8824388 , -0.9266356 ],
                        [-0.61939514,  0.23290041],
                       [-0.4848329 ,  1.111317  ]]]
                      , dtype=np.float32)
    np.random.seed(1)
    swarm = Swarm()
    swarm.init_pspace('data/pspace_multi_line.txt')
    swarm.init_particles(2)
    np.testing.assert_equal(swarm.current, output)

def test_get_gbest_full():
    """
    swarm.get_best tests.
    """
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)


    np.random.seed(1)
    swarm = Swarm()
    swarm.init_pspace('data/pspace_one_line.txt')
    swarm.init_particles(9)
    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0
    np.testing.assert_equal(swarm.get_gbest(topology='full'), output)

def test_get_gbest_ring():
    """
    swarm.get_best tests.
    """
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)


    np.random.seed(1)
    swarm = Swarm()
    swarm.init_pspace('data/pspace_one_line.txt')
    swarm.init_particles(9)
    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0
    np.testing.assert_equal(swarm.get_gbest(topology='ring', indv=4), output)

def test_get_gbest_toroidal():
    """
    swarm.get_best tests.
    """
    output = np.array([[-0.4848329 ,  1.111317  ]], dtype=np.float32)

    np.random.seed(1)
    swarm = Swarm()
    swarm.init_pspace('data/pspace_one_line.txt')
    swarm.init_particles(9)
    # Fake evaluation
    swarm.history[:, :, :] = swarm.current[:, :, :]
    swarm.misfit[:] = 1.0
    swarm.misfit[5] = 0.0
    np.testing.assert_equal(swarm.get_gbest(topology='toroidal', indv=8, ndim=3), output)

if __name__ == "__main__" :
    np.testing.run_module_suite()