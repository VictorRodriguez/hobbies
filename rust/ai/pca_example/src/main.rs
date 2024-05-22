use ndarray::{array, Array2, Axis};
use ndarray_linalg::{eigh::Eigh, UPLO};

fn pca(data: &Array2<f64>, n_components: usize) -> (Array2<f64>, Array2<f64>) {
    let (n_samples, n_features) = data.dim();
    assert!(n_components <= n_features, "n_components must be less than or equal to the number of features");

    // Center the data
    let mean = data.mean_axis(Axis(0)).unwrap();
    let centered_data = data - &mean;

    // Compute covariance matrix
    let covariance_matrix = centered_data.t().dot(&centered_data) / (n_samples as f64 - 1.0);

    // Eigen decomposition
    let (eigenvalues, eigenvectors) = covariance_matrix.eigh(UPLO::Lower).unwrap();

    // Sort eigenvalues and eigenvectors
    let mut eigen_pairs: Vec<(f64, Array2<f64>)> = eigenvalues.iter()
        .zip(eigenvectors.axis_iter(Axis(1)))
        .map(|(val, vec)| (*val, vec.to_owned().insert_axis(Axis(1))))
        .collect();
    eigen_pairs.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

    // Select top n_components
    let top_eigenvectors: Array2<f64> = eigen_pairs.iter()
        .take(n_components)
        .map(|(_, vec)| vec.to_owned())
        .fold(Array2::<f64>::zeros((n_features, 0)), |acc, vec| {
            ndarray::concatenate![Axis(1), acc, vec]
        });

    // Project data onto top eigenvectors
    let projected_data = centered_data.dot(&top_eigenvectors);

    (projected_data, top_eigenvectors)
}

fn main() {
    // Example data
    let data: Array2<f64> = array![
        [2.5, 2.4],
        [0.5, 0.7],
        [2.2, 2.9],
        [1.9, 2.2],
        [3.1, 3.0],
        [2.3, 2.7],
        [2.0, 1.6],
        [1.0, 1.1],
        [1.5, 1.6],
        [1.1, 0.9]
    ];

    // Perform PCA
    let n_components = 2;
    let (projected_data, components) = pca(&data, n_components);

    // Print results
    println!("Projected data:\n{:.4}", projected_data);
    println!("Principal components:\n{:.4}", components);
}

