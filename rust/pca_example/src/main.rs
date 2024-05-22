use linfa::Dataset;
use linfa_reduction::pca::Pca;
use ndarray::array;

fn main() {
    // Input data
    let x = array![[1.0, 2.0],
                   [3.0, 4.0]];

    // Create Dataset
    let dataset = Dataset::from(x);

    // Create PCA instance with the number of components
    let pca = Pca::params(2)
        .fit(&dataset)
        .expect("PCA fitting failed");

    // Project data
    let transformed = pca.transform(&dataset);

    // Print the transformed data
    println!("Transformed data:\n{:?}", transformed);
}

