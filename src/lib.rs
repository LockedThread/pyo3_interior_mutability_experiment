use pyo3::prelude::*;
use std::sync::RwLock;

/// A pure Rust struct we'll wrap for Python.
pub struct OtherStruct {
    pub x: i32,
}

/// Python-visible wrapper with interior mutability.
#[pyclass]
pub struct PyOtherStruct {
    inner: RwLock<OtherStruct>,
}

#[pymethods]
impl PyOtherStruct {
    /// Python constructor: PyOtherStruct(x: int)
    #[new]
    fn new(x: i32) -> Self {
        PyOtherStruct {
            inner: RwLock::new(OtherStruct { x }),
        }
    }

    /// Getter for `x` (attribute access in Python).
    #[getter]
    fn x(&self) -> PyResult<i32> {
        Ok(self
            .inner
            .read()
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("RwLock poisoned"))?
            .x)
    }

    /// Setter for `x` (assignment in Python).
    #[setter]
    fn set_x(&self, val: i32) -> PyResult<()> {
        self.inner
            .write()
            .map_err(|_| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("RwLock poisoned"))?
            .x = val;
        Ok(())
    }

    /// String representation for Python's str()
    fn __str__(&self) -> PyResult<String> {
        self.__repr__()
    }

    /// String representation for Python's repr()
    fn __repr__(&self) -> PyResult<String> {
        let x = self.x()?;
        Ok(format!("PyOtherStruct(x={})", x))
    }
}

/// A container of PyOtherStruct wrappers.
#[pyclass]
pub struct PyMyStruct {
    items: Vec<Py<PyOtherStruct>>,
}

#[pymethods]
impl PyMyStruct {
    /// Python constructor: PyMyStruct([PyOtherStruct, ...])
    #[new]
    fn new(wrappers: Vec<Py<PyOtherStruct>>) -> Self {
        PyMyStruct { items: wrappers }
    }

    /// Getter for `items_py`, returns the same wrapper instances each time.
    #[getter]
    fn items_py<'py>(&self, py: Python<'py>) -> Vec<Py<PyOtherStruct>> {
        // clone_ref bumps the reference count on each Py<PyOtherStruct>
        self.items.iter().map(|o| o.clone_ref(py)).collect()
    }

    /// String representation for Python's str()
    fn __str__<'py>(&self, py: Python<'py>) -> PyResult<String> {
        self.__repr__(py)
    }

    /// String representation for Python's repr()
    fn __repr__<'py>(&self, py: Python<'py>) -> PyResult<String> {
        let mut items_str = String::from("[");
        for (i, item) in self.items.iter().enumerate() {
            if i > 0 {
                items_str.push_str(", ");
            }
            let item_ref = item.bind(py);
            let item_repr = item_ref.repr()?.to_string();
            items_str.push_str(&item_repr);
        }
        items_str.push(']');
        Ok(format!("PyMyStruct({})", items_str))
    }
}

/// The Python module definition. Name must match your Cargo.toml `name` entry.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyOtherStruct>()?;
    m.add_class::<PyMyStruct>()?;
    Ok(())
}
