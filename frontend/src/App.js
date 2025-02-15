import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TopBar from "./components/TopBar";
import Home from "./pages/Home";
import Plataforma from "./pages/Plataforma";
import PlataformaResumo from "./pages/PlataformaResumo";
import Geral from "./pages/Geral";
import GeralResumo from "./pages/GeralResumo";
import "./App.css";

function App() {
    return (
        <Router>
            <TopBar />
            <div style={{ padding: "20px" }}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/:plataforma" element={<Plataforma />} />
                    <Route
                        path="/:plataforma/resumo"
                        element={<PlataformaResumo />}
                    />
                    <Route path="/geral" element={<Geral />} />
                    <Route path="/geral/resumo" element={<GeralResumo />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
