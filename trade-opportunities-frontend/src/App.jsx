import { useState } from "react";
import ReactMarkdown from "react-markdown";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [sector, setSector] = useState("technology");
  const [apiKey, setApiKey] = useState("test-client-123");
  const [reportMarkdown, setReportMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleGenerateReport = async () => {
    // Basic client-side validation
    const trimmedSector = sector.trim();
    if (!trimmedSector) {
      setErrorMessage("Please enter a sector.");
      return;
    }

    setLoading(true);
    setErrorMessage("");
    setReportMarkdown("");

    try {
      const res = await fetch(
        `${API_BASE_URL}/analyze/${encodeURIComponent(trimmedSector)}`,
        {
          method: "GET",
          headers: {
            "X-API-Key": apiKey.trim(),
          },
        }
      );

      if (!res.ok) {
        if (res.status === 401) {
          setErrorMessage("Unauthorized: Please provide a valid X-API-Key.");
        } else if (res.status === 429) {
          setErrorMessage(
            "Rate limit exceeded: Please wait a minute before trying again."
          );
        } else if (res.status === 400) {
          const data = await res.json().catch(() => null);
          setErrorMessage(
            data?.detail || "Bad request: Please check the sector value."
          );
        } else {
          setErrorMessage(
            `Unexpected error: ${res.status} ${res.statusText}`
          );
        }
        return;
      }

      const data = await res.json();
      setReportMarkdown(data.report_markdown || "");
    } catch (err) {
      console.error(err);
      setErrorMessage("Network error: Unable to reach the API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#0f172a",
        color: "#e5e7eb",
        fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
        padding: "24px",
      }}
    >
      <div
        style={{
          maxWidth: "960px",
          margin: "0 auto",
        }}
      >
        <header style={{ marginBottom: "24px" }}>
          <h1 style={{ fontSize: "28px", marginBottom: "8px" }}>
            Trade Opportunities Dashboard
          </h1>
          <p style={{ color: "#9ca3af" }}>
            Analyze Indian sector trade opportunities using the FastAPI + Gemini
            backend.
          </p>
        </header>

        <section
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "12px",
            marginBottom: "24px",
            padding: "16px",
            backgroundColor: "#111827",
            borderRadius: "8px",
            border: "1px solid #1f2937",
          }}
        >
          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <div style={{ flex: "1 1 200px" }}>
              <label
                htmlFor="sector"
                style={{ display: "block", marginBottom: "4px" }}
              >
                Sector
              </label>
              <input
                id="sector"
                type="text"
                value={sector}
                onChange={(e) => setSector(e.target.value)}
                placeholder="e.g. technology, pharmaceuticals, agriculture"
                style={{
                  width: "100%",
                  padding: "8px",
                  borderRadius: "4px",
                  border: "1px solid #4b5563",
                  backgroundColor: "#020617",
                  color: "#e5e7eb",
                }}
              />
            </div>

            <div style={{ flex: "1 1 200px" }}>
              <label
                htmlFor="apiKey"
                style={{ display: "block", marginBottom: "4px" }}
              >
                X-API-Key
              </label>
              <input
                id="apiKey"
                type="text"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="e.g. test-client-123"
                style={{
                  width: "100%",
                  padding: "8px",
                  borderRadius: "4px",
                  border: "1px solid #4b5563",
                  backgroundColor: "#020617",
                  color: "#e5e7eb",
                }}
              />
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <button
              onClick={handleGenerateReport}
              disabled={loading}
              style={{
                padding: "10px 18px",
                borderRadius: "6px",
                border: "none",
                backgroundColor: loading ? "#4b5563" : "#2563eb",
                color: "#f9fafb",
                fontWeight: 500,
                cursor: loading ? "not-allowed" : "pointer",
              }}
            >
              {loading ? "Generating..." : "Generate Report"}
            </button>
            {loading && (
              <span style={{ color: "#9ca3af", fontSize: "14px" }}>
                Contacting backend (GNews + Gemini)...
              </span>
            )}
          </div>

          {errorMessage && (
            <div
              style={{
                marginTop: "8px",
                padding: "8px 12px",
                borderRadius: "4px",
                backgroundColor: "#7f1d1d",
                color: "#fee2e2",
                fontSize: "14px",
              }}
            >
              {errorMessage}
            </div>
          )}
        </section>

        <section
          style={{
            padding: "16px",
            backgroundColor: "#020617",
            borderRadius: "8px",
            border: "1px solid #1f2937",
          }}
        >
          <h2 style={{ fontSize: "20px", marginBottom: "12px" }}>
            Report Output
          </h2>

          {!reportMarkdown && !loading && !errorMessage && (
            <p style={{ color: "#6b7280", fontSize: "14px" }}>
              Enter a sector and click &quot;Generate Report&quot; to view the
              analysis.
            </p>
          )}

          {reportMarkdown && (
            <div
              style={{
                marginTop: "8px",
                padding: "16px",
                borderRadius: "8px",
                backgroundColor: "#020617",
                border: "1px solid #111827",
                maxHeight: "70vh",
                overflowY: "auto",
              }}
            >
              <ReactMarkdown
                components={{
                  h1: ({ node, ...props }) => (
                    <h1
                      style={{
                        fontSize: "24px",
                        marginBottom: "12px",
                        color: "#e5e7eb",
                      }}
                      {...props}
                    />
                  ),
                  h2: ({ node, ...props }) => (
                    <h2
                      style={{
                        fontSize: "18px",
                        marginTop: "16px",
                        marginBottom: "8px",
                        color: "#facc15",
                      }}
                      {...props}
                    />
                  ),
                  li: ({ node, ...props }) => (
                    <li style={{ marginBottom: "4px" }} {...props} />
                  ),
                  a: ({ node, ...props }) => (
                    <a
                      style={{ color: "#38bdf8" }}
                      target="_blank"
                      rel="noreferrer"
                      {...props}
                    />
                  ),
                }}
              >
                {reportMarkdown}
              </ReactMarkdown>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;