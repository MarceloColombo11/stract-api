import React, { useState, useEffect } from "react";

const platformOptions = [
    { text: "Facebook Ads", value: "meta_ads" },
    { text: "Google Analytics", value: "ga4" },
    { text: "TikTok", value: "tiktok_insights" },
];

function Plataforma() {
    const [selectedPlatform, setSelectedPlatform] = useState("");
    const [tableData, setTableData] = useState([]);
    const [columns, setColumns] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (selectedPlatform !== "") {
            setLoading(true);
            setError(null);
            fetch(`http://127.0.0.1:5000/${selectedPlatform}/resumo`)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Erro na requisição");
                    }
                    return response.json();
                })
                .then((json) => {
                    setTableData(json);
                    // Se houver dados, determina as colunas dinamicamente
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
    }, [selectedPlatform]);

    return (
        <div style={{ padding: "20px" }}>
            <h1>Resumo da Plataforma</h1>
            <div style={{ marginBottom: "20px" }}>
                <label
                    htmlFor="platform-select"
                    style={{ marginRight: "10px" }}
                >
                    Escolha a Plataforma:
                </label>
                <select
                    id="platform-select"
                    value={selectedPlatform}
                    onChange={(e) => setSelectedPlatform(e.target.value)}
                    style={{ padding: "5px", fontSize: "1rem" }}
                >
                    <option value="">Selecione...</option>
                    {platformOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                            {option.text}
                        </option>
                    ))}
                </select>
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
