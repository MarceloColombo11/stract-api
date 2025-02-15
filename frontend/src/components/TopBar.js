import React from "react";
import { Link } from "react-router-dom";
import "./TopBar.css"; // Crie este arquivo para estilos personalizados

function TopBar() {
    return (
        <nav className="top-bar">
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                {/* Supondo que "plataforma" seja um valor fixo para o exemplo */}
                <li>
                    <Link to="/plataforma">Plataforma</Link>
                </li>
                <li>
                    <Link to="/plataforma/resumo">Resumo Plataforma</Link>
                </li>
                <li>
                    <Link to="/geral">Geral</Link>
                </li>
                <li>
                    <Link to="/geral/resumo">Resumo Geral</Link>
                </li>
            </ul>
        </nav>
    );
}

export default TopBar;
