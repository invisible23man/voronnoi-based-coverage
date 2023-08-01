from sklearn.mixture import BayesianGaussianMixture
from sklearn.neighbors import KernelDensity

def set_sensor_estimation_model(method='kde'):
    if method == 'truncated_gmm':
        return TruncatedGMM(n_components=10)
    elif method == 'kde':
        return KernelDensity(kernel='gaussian', bandwidth=0.6)
    elif method == 'dpmm':
        return BayesianGaussianMixture(n_components=2,
                                       weight_concentration_prior_type="dirichlet_process")
    else:
        raise ValueError(f"Unknown method: {method}")

"""
Dirichlet Process Mixture Models (DPMMs) are a type of Bayesian nonparametric model. They allow for flexible cluster assignments and don't require you to specify the number of clusters in advance. Instead, the DPMM will attempt to find an appropriate number of clusters based on the data.

However, DPMMs do have several hyperparameters that can significantly impact the model's behavior. For instance, the weight_concentration_prior_type and weight_concentration_prior parameters control the distribution of the mixture weights and can influence the number of clusters that the model infers. Specifically, a larger value of weight_concentration_prior will encourage the model to use more clusters.

Another hyperparameter of importance in DPMMs is the n_components parameter, which sets the maximum number of mixture components that the model can use. While DPMMs don't require you to know the number of clusters in advance, setting n_components to a value larger than the expected number of clusters can help ensure that the model has enough flexibility to capture all the clusters in the data.

The init_params and n_init parameters can also be important. init_params controls the method used to initialize the model's parameters, while n_init sets the number of times the model will be initialized with different parameter settings. The model will keep the parameters that give the highest likelihood over the n_init runs.

DPMMs can be sensitive to the choice of these hyperparameters, so it can be helpful to experiment with different settings to see what works best for your specific data. You may also want to consider using a validation set or cross-validation to tune these hyperparameters.
"""

from sklearn.mixture import GaussianMixture
from scipy.stats import multivariate_normal
import numpy as np

class TruncatedGMM:
    def __init__(self, n_components=10):
        self.n_components = n_components
        self.gmm = GaussianMixture(n_components=n_components)
        self.truncated_gaussians = []

    def fit(self, path, X):
        # Fit the GMM to the data
        self.gmm.fit(X.reshape(-1,1))

        # Create a list of truncated multivariate normal distributions
        self.truncated_gaussians = [
            multivariate_normal(mean=mean, cov=cov)
            for mean, cov in zip(self.gmm.means_, self.gmm.covariances_)
        ]

    def predict(self, X):
        # Compute the sum of the PDFs of the truncated gaussians for each data point
        densities = np.sum([
            gaussian.pdf(X) for gaussian in self.truncated_gaussians
        ], axis=0)

        return densities
