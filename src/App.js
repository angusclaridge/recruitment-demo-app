import React from "react";
import Dropzone from "./dropzone";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter, Link, Routes, Route } from "react-router-dom";
import ItemsTable from "./CandidatesTable";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <h1>Upload Candidate Audio</h1>
        <Dropzone />
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          closeOnClick
          pauseOnHover
          draggable
          pauseOnFocusLoss
          theme="light"
        />
        <Link to="/items">View Candidates</Link>
      </div>
      <Routes>
        <Route path="/items" element={<ItemsTable />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
