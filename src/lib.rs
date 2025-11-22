use pyo3::prelude::*;
use ustar::{default_config, parse};
use std::fs;

#[pyfunction]
fn validate_star_string(content: &str) -> PyResult<String> {
    let config = default_config();
    
    match parse(content, &config) {
        Ok(result) => Ok(format!("Parsed successfully: rule={}, span={}-{}", 
                                result.rule_name, result.start, result.end)),
        Err(e) => Err(pyo3::exceptions::PyValueError::new_err(format!("Parse error: {}", e))),
    }
}

#[pyfunction]
fn validate_star_file(path: &str) -> PyResult<String> {
    let config = default_config();
    
    match fs::read_to_string(path) {
        Ok(content) => {
            match parse(&content, &config) {
                Ok(result) => Ok(format!("Parsed file '{}' successfully: rule={}, span={}-{}", 
                                        path, result.rule_name, result.start, result.end)),
                Err(e) => Err(pyo3::exceptions::PyValueError::new_err(format!("Parse error: {}", e))),
            }
        }
        Err(e) => Err(pyo3::exceptions::PyIOError::new_err(format!("File error: {}", e))),
    }
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(validate_star_string, m)?)?;
    m.add_function(wrap_pyfunction!(validate_star_file, m)?)?;
    Ok(())
}