import { BrowserRouter, Route, Routes } from "react-router";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Datasets from "./pages/Datasets";
import DatasetDetail from "./pages/DatasetDetail";
import Results from "./pages/Results";
import ResultDetail from "./pages/ResultDetail";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/datasets/:id" element={<DatasetDetail />} />
          <Route path="/results" element={<Results />} />
          <Route path="/results/:id" element={<ResultDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
