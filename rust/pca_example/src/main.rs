//use linfa::Dataset;
//use ndarray::array;
use linfa::traits::{Fit, Predict};
use linfa_reduction::Pca;

fn main() {
    // Input data
    //let x = array![[1.0, 2.0],
    //               [3.0, 4.0]];
    //let dataset = Dataset::from(x);

    // Create Dataset
    let dataset = linfa_datasets::iris();

    // Create PCA instance with the number of components
    let pca = Pca::params(2)
        .fit(&dataset).unwrap();

    // Project data
    let transformed = pca.predict(dataset);

    // Print the transformed data
    println!("Transformed data:\n{:?}", transformed);

}

