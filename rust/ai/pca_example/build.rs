// build.rs
fn main() {
    println!("cargo:rustc-link-lib=openblas");
}
