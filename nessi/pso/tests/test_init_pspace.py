import numpy as np
from nessi.pso import init_pspace


def test_init_pspace_one_line():
    """
    pso_init_pspace test for one point search.
    """
    pspace_output = np.zeros((1, 2, 3), dtype=np.float32)
    pspace_output[0,0,0] = -3.0
    pspace_output[0,0,1] = 3.0
    pspace_output[0,0,2] = 0.6
    pspace_output[0,1,0] = -3.0
    pspace_output[0,1,1] = 3.0
    pspace_output[0,1,2] = 0.6
    pspace_one_line = init_pspace('data/pspace_one_line.txt')
    np.testing.assert_equal(pspace_one_line, pspace_output)

def test_init_pspace_multi_line():
    """
    pso_init_pspace test for multipoint search.
    """
    pspace_output = np.zeros((3, 2, 3), dtype=np.float32)
    pspace_output[0,0,0] = -3.0
    pspace_output[0,0,1] = 3.0
    pspace_output[0,0,2] = 0.6
    pspace_output[0,1,0] = -3.0
    pspace_output[0,1,1] = 3.0
    pspace_output[0,1,2] = 0.6
    pspace_output[1,0,0] = -3.0
    pspace_output[1,0,1] = 3.0
    pspace_output[1,0,2] = 0.6
    pspace_output[1,1,0] = -3.0
    pspace_output[1,1,1] = 3.0
    pspace_output[1,1,2] = 0.6
    pspace_output[2,0,0] = -3.0
    pspace_output[2,0,1] = 3.0
    pspace_output[2,0,2] = 0.6
    pspace_output[2,1,0] = -3.0
    pspace_output[2,1,1] = 3.0
    pspace_output[2,1,2] = 0.6
    pspace_one_line = init_pspace('data/pspace_multi_line.txt')
    np.testing.assert_equal(pspace_one_line, pspace_output)
    
if __name__ == "__main__" :
    np.testing.run_module_suite()
