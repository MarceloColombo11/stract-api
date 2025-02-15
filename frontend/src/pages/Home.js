import React, { useEffect, useState } from "react";
import "../styles/Home.css";

function App() {
    const [dados, setDados] = useState([]);

    useEffect(() => {
        fetch("http://127.0.0.1:5000/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Erro na requisição");
                }
                return response.json();
            })
            .then((json) => setDados(json))
            .catch((error) => console.error("Erro:", error));
    }, []);

    return (
        <div className="container">
            <h1 className="title">Stract</h1>
            {dados.length === 0 ? (
                <p>Carregando...</p>
            ) : (
                <ul className="list">
                    {dados.map((item, index) => (
                        <li key={index} className="item">
                            <p>
                                <strong>Nome:</strong> {item.Nome}
                            </p>
                            <p>
                                <strong>E-mail:</strong> {item["E-mail"]}
                            </p>
                            <p>
                                <strong>Linkedin:</strong>{" "}
                                <a
                                    className="link"
                                    href={item.Linkedin}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {item.Linkedin}
                                </a>
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default App;
