import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/home/Home";

export class Rotas extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <Routes>
          <Route element={<Home />} path="/" exact />
        </Routes>
      </BrowserRouter>
    );
  }
}

export default Rotas;
