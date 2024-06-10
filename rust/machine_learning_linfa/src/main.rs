use linfa::traits::{Fit, Predict};
use linfa::DatasetBase;
use linfa_clustering::KMeans;
use linfa_nn::distance::LInfDist;
use ndarray::{Axis, ArrayBase, OwnedRepr, Dim};
use polars::prelude::*;
use ndarray_rand::rand::SeedableRng;
use rand_xoshiro::Xoshiro256Plus;
use plotters::prelude::*;

fn main() {
    // Our random number generator, seeded for reproducibility
    let  rng = Xoshiro256Plus::seed_from_u64(42);

    // Read the iris dataset using Polars
    let df = CsvReader::from_path("/Users/vrodri3/devel/hobbies/rust/machine_learning_linfa/iris.csv")
        .unwrap()
        .infer_schema(None)
        .has_header(true)
        .finish()
        .unwrap();


    let features= df.to_ndarray::<Float64Type>(IndexOrder::C);

    // Create a dataset
    let dataset = DatasetBase::from(features.unwrap());

    // Configure the KMeans algorithm
    let n_clusters = 3; // Assuming we want to identify 3 clusters
    let model = KMeans::params_with(n_clusters, rng, LInfDist)
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
    let colors = [RED, BLUE, GREEN];

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
