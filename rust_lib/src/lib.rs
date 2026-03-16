use pyo3::prelude::*;
use std::collections::HashSet;

/// Calculates the Jaccard similarity between two strings.
/// Returns a float between 0.0 (completely different) and 1.0 (identical).
#[pyfunction]
fn jaccard_similarity(text1: &str, text2: &str) -> f64 {
    // Split texts into words and store them in HashSets for fast comparison
    let set1: HashSet<&str> = text1.split_whitespace().collect();
    let set2: HashSet<&str> = text2.split_whitespace().collect();

    // Count the number of common words (intersection)
    let intersection = set1.intersection(&set2).count();
    
    // Count the total number of unique words across both texts (union)
    let union = set1.union(&set2).count();

    // Prevent division by zero if both texts are empty
    if union == 0 {
        return 0.0;
    }

    // Calculate the Jaccard index
    intersection as f64 / union as f64
}

/// This module initializes the Rust library for Python.
/// The function name must match the module name.
#[pymodule]
fn rust_lib(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add the Jaccard similarity function to the Python module
    m.add_function(wrap_pyfunction!(jaccard_similarity, m)?)?;
    Ok(())
}