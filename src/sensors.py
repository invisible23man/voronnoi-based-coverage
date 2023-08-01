from sklearn.mixture import BayesianGaussianMixture
from sklearn.neighbors import KernelDensity

def set_sensor_estimation_model(method='kde'):
    if method == 'kde':
        return KernelDensity(kernel='gaussian', bandwidth=0.2)
    elif method == 'dpmm':
        return BayesianGaussianMixture(weight_concentration_prior_type="dirichlet_process")
    else:
        raise ValueError(f"Unknown method: {method}")
