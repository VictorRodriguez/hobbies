use linfa::traits::{Fit, Predict};
use linfa_reduction::Pca;
use linfa_clustering::{KMeans};

fn main() {

    let dataset = linfa_datasets::iris();

    let pca = Pca::params(2)
        .fit(&dataset)
        .expect("PCA failing");

    let transformed = pca.predict(dataset.clone());

    let new_points = transformed.records();

    println!("{:?}", new_points);

    let cluster_range = 1..10;
    let mut inertias = Vec::new();

	println!("\n Inertias per cluster:");
    for n_clusters in cluster_range.clone() {
        let _model = KMeans::params(n_clusters)
        .fit(&dataset)
        .expect("KMeans fitted");
        let _inertia = _model.inertia();
        inertias.push((n_clusters, _inertia));
        println!("Inertia with {} clusters = {:?}",n_clusters,_inertia);
    }

    let optimal_k = find_elbow(&inertias);
    println!("\nOptimal number of clusters (elbow point): {}", optimal_k);


	let _model = KMeans::params(optimal_k)
		.fit(&dataset)
		.expect("KMeans fitted");

	// Get the labels assigned to each data point
    let labels = _model.predict(&dataset);

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

