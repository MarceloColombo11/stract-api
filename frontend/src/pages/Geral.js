import React, { useState, useEffect } from "react";

function Plataforma() {
    const [tableData, setTableData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        {
            setLoading(true);
            setError(null);
            fetch(`http://127.0.0.1:5000/geral`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Erro na requisição");
                    }
                    return response.json();
                })
                .then((json) => {
                    setTableData(json);
                    if (json.length > 0) {
                        const cols = Object.keys(json[0]);
                        setColumns(cols);
                    } else {
                        setColumns([]);
                    }
                    setLoading(false);
                })
                .catch((err) => {
                    console.error("Erro:", err);
                    setError("Erro ao carregar os dados.");
                    setLoading(false);
                });
        }
    }, []);

    return (
        <div style={{ padding: "20px" }}>
            <h1>Geral</h1>
            <div style={{ marginBottom: "20px" }}>
                <label
                    htmlFor="platform-select"
                    style={{ marginRight: "10px" }}
                >
                    Informações de todas as plataformas:
                </label>
            </div>

            {loading && <p>Carregando...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}

            {tableData.length > 0 && !loading && (
                <div style={{ overflowX: "auto" }}>
                    <table
                        style={{ width: "100%", borderCollapse: "collapse" }}
                    >
                        <thead>
                            <tr>
                                {columns.map((col, index) => (
                                    <th
                                        key={index}
                                        style={{
                                            border: "1px solid #ddd",
                                            padding: "8px",
                                            backgroundColor: "#f2f2f2",
                                            textTransform: "capitalize",
                                        }}
                                    >
                                        {col}
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.map((row, index) => (
                                <tr key={index}>
                                    {columns.map((col, idx) => (
                                        <td
                                            key={idx}
                                            style={{
                                                border: "1px solid #ddd",
                                                padding: "8px",
                                            }}
                                        >
                                            {row[col]}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default Plataforma;
