use linfa::traits::{Fit, Predict};
use linfa::DatasetBase;
use linfa_clustering::KMeans;
use linfa_nn::distance::LInfDist;
use ndarray::{Axis, ArrayBase, OwnedRepr, Dim};
use polars::prelude::*;
use ndarray_rand::rand::SeedableRng;
use rand_xoshiro::Xoshiro256Plus;
use ndarray::Array2;
use std::env;
use plotters::prelude::*;

fn find_optimal_number_of_clusters(inertias: &[(usize, f64)]) -> usize {
    // Calculate differences between consecutive inertias
    let differences: Vec<f64> = inertias
        .iter()
        .map(|&(n, inertia)| inertia)
        .collect::<Vec<_>>()
        .windows(2)
        .map(|w| w[1] - w[0])
        .collect();

    // Calculate second differences
    let second_differences: Vec<f64> = differences
        .windows(2)
        .map(|w| w[1] - w[0])
        .collect();

    // Find index of maximum second difference
    let elbow_index = second_differences
        .iter()
        .enumerate()
        .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
        .map(|(i, _)| i);

    // Return optimal number of clusters (adding 2 because differences is 1 element shorter than inertias)
    elbow_index.unwrap() + 2
}


fn main() {

	let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        eprintln!("Usage: {} <file_path> <column to exclude>", args[0]);
        std::process::exit(1);
    }

    let file_path = &args[1];
    let column = &args[2];

    // Our random number generator, seeded for reproducibility
    let  rng = Xoshiro256Plus::seed_from_u64(42);

    // Read the iris dataset using Polars
    let df = CsvReader::from_path(file_path)
        .unwrap()
        .infer_schema(None)
        .has_header(true)
        .finish()
        .unwrap();


    let filtered_df = df.drop(column).unwrap(); // Drop the excluded column from the DataFrame
    let features = filtered_df.to_ndarray::<Float64Type>(IndexOrder::C);

    //let features= df.to_ndarray::<Float64Type>(IndexOrder::C);

    // Create a dataset
    let dataset = DatasetBase::from(features.unwrap());
	println!("Printing Dataset");
	println!("{:?}",dataset);

    // Configure the KMeans algorithm
    //let n_clusters = 3; // Assuming we want to identify 3 clusters

    let max_clusters = 10;
    let mut inertias = Vec::new();
    let cluster_range = 1..=max_clusters;

    println!("\nInertias per cluster:");
    for n_clusters in cluster_range.clone() {
        let model = KMeans::params_with(n_clusters, rng.clone(), LInfDist)
            .max_n_iterations(200)
            .tolerance(1e-5)
            .fit(&dataset.clone())
            .expect("KMeans fitted");
        let inertia = model.inertia();
        inertias.push((n_clusters, inertia));
        println!("Inertia with {} clusters = {:?}", n_clusters, inertia);
    }

    let optimal_clusters = find_optimal_number_of_clusters(&inertias);

    println!("optimal_clusters = {optimal_clusters}");

    let model = KMeans::params_with(optimal_clusters, rng, LInfDist)
        .max_n_iterations(200)
        .tolerance(1e-5)
        .fit(&dataset)
        .expect("KMeans fitted");

    // Predict the clusters
    let predictions = model.predict(dataset);

    // print the predictions

    println!("{:?}", predictions);

    // plot these predictions in a graph with plotters

    println!("Plotting predictions");

    // Create a drawing area and configure the plot
    let root = BitMapBackend::new("plot.png", (600, 400)).into_drawing_area();
    let _ = root.fill(&WHITE);
    let mut chart = ChartBuilder::on(&root)
        .caption("Plotting K-Means Clusters", ("sans-serif", 40).into_font())
        .margin(5)
        .x_label_area_size(30)
        .y_label_area_size(30)
        .build_cartesian_2d(0f32..10f32, 0f32..10f32)
        .unwrap();

    let _ = chart.configure_mesh().draw();

    // Define colors for each cluster
    let colors = [RED, BLUE, GREEN, YELLOW];


    let records: ArrayBase<OwnedRepr<f64>, Dim<[usize; 2]>> = predictions.records().clone();
    let targets = predictions.targets();

    println!("{:?}", records);
    println!("{:?}", targets);

    // Make a vector of tuples (f32, f32)
    let mut data: Vec<(f32, f32)> = Vec::new();

    for (record, target) in records.axis_iter(Axis(0)).zip(targets) {

        // Replace data
        data = Vec::new();
        data.push((record[0] as f32, record[1] as f32)); // Selecting "sepal.length" and "sepal.width"

        chart
        .draw_series(PointSeries::of_element(
            data.clone(),
            5,
            ShapeStyle::from(
                &colors[*target as usize]).filled(),
                &|coord, size, style| {
                EmptyElement::at(coord) + Circle::new((0, 0), size, style.filled())
            },
        ))
        .unwrap();
    }


}
