use linfa::traits::{Fit, Predict};
use linfa_reduction::Pca;
use linfa_clustering::{KMeans};

use std::error::Error;
use std::fs::File;
use std::io::Read;
use csv::ReaderBuilder;
use ndarray::Array2;

use ndarray::{Axis, array, s};
use linfa::dataset::DatasetBase;


fn main() {

    // Read the CSV file
    let (array, header) = match read_csv("iris.csv") {
        Ok(result) => result,
        Err(err) => {
            eprintln!("Error reading CSV file: {}", err);
            return;
        }
    };

    println!("Header: {:?}", header);
    println!("Data Array:\n{:?}", array);

    // Create a new array with the specified column removed
    let new_array = drop_column(array, 0);

    // Create a new dataset
    let dataset = DatasetBase::from(new_array);

    // apply PCA projection along a line which maximizes the spread of the data
    let embedding = Pca::params(2).fit(&dataset).unwrap();

    // reduce dimensionality of the dataset
    let new_points = embedding.predict(dataset.clone());

    let DatasetBase {
        records, targets, ..
    } = new_points.clone();

    let targets_db = DatasetBase::from(targets.clone());

    println!("Printing PCA data");
    println!("Targets: {:?}", targets_db);

    let cluster_range = 1..10;
    let mut inertias = Vec::new();

	println!("\n Inertias per cluster:");
    for n_clusters in cluster_range.clone() {
        let _model = KMeans::params(n_clusters)
        .fit(&targets_db)
        .expect("KMeans fitted");
        let _inertia = _model.inertia();
        inertias.push((n_clusters, _inertia));
        println!("Inertia with {} clusters = {:?}",n_clusters,_inertia);
    }

    let optimal_k = find_elbow(&inertias);
    println!("\nOptimal number of clusters (elbow point): {}", optimal_k);

	let _model = KMeans::params(optimal_k)
		.fit(&targets_db)
		.expect("KMeans fitted");

	// Get the labels assigned to each data point
    let labels = _model.predict(&targets_db);
    println!("Labels:\n{}", labels);

	// Get the centroids
    let centroids = &_model.centroids();
    println!("Centroids:\n{}", centroids);

    // Print centroids
    for centroid in centroids.outer_iter() {
        let x = centroid[0];
        let y = centroid[1];
        println!("Centroid: ({}, {})", x, y);
    }


	for (i, label) in labels.iter().enumerate() {
        println!("Element {}: Label {}", i, label);
    }


}

fn find_elbow(inertias: &[(usize, f64)]) -> usize {
    let mut prev_inertia = f64::MAX;
    let mut best_k = 1;
    for &(k, inertia) in inertias {
        let diff = prev_inertia / inertia;
        if diff < 1.5 {
            // If the ratio falls below 1.5, consider it as the elbow point
            best_k = k;
            break;
        }
        prev_inertia = inertia;
    }
    best_k
}

// Function to read a CSV file into an ndarray along with its header
fn read_csv(file_path: &str) -> Result<(Array2<f64>, Vec<String>), Box<dyn Error>> {
    let mut reader = ReaderBuilder::new()
        .has_headers(true)
        .from_path(file_path)?;

    // Read the header
    let header = reader.headers()?.iter().map(|s| s.to_string()).collect();

    let mut records = Vec::new();

    for result in reader.records() {
        let record = result?;
        let parsed_record: Vec<f64> = record.iter()
            .take(5) // Exclude the species column
            .map(|field| field.parse().expect("Failed to parse field"))
            .collect();
        records.push(parsed_record);
    }

    // Determine the shape of the resulting array
    let num_rows = records.len();
    let num_cols = records[0].len();
    let flat_data: Vec<f64> = records.into_iter().flatten().collect();

    let array = Array2::from_shape_vec((num_rows, num_cols), flat_data)?;

    Ok((array, header))
}

fn drop_column(array: Array2<f64>, column_to_drop: usize) -> Array2<f64> {
    let shape = array.shape();
    let (nrows, ncols) = (shape[0], shape[1]);

    // Create a new array with one less column
    let mut new_array = Array2::<f64>::zeros((nrows, ncols - 1));

    for i in 0..nrows {
        for j in 0..column_to_drop {
            new_array[[i, j]] = array[[i, j]];
        }
        for j in column_to_drop + 1..ncols {
            new_array[[i, j - 1]] = array[[i, j]];
        }
    }

    new_array
}
