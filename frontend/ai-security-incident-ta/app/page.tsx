"use client";

import { useState } from "react";

type Alert = {
  event_id: string;
  ip: string;
  threat_type: string;
  severity: string;
  risk_score: number;
  timestamp: string;
  explanation: string;
};

export default function SOCDashboard() {
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<Alert[]>([]);

  // Use env variable or fallback to local backend
  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

  const runAgent = async () => {
    setLoading(true);
    setOutput("");

    const event_id = (history.length + 1).toString();
    const timestamp = new Date().toISOString();

    const event = {
      event_id,
      event: "Multiple failed login attempts detected",
      logs: "failed login attempts from IP 192.168.1.10",
      source: "auth-system",
      timestamp,
    };

    try {
      const res = await fetch(`${BACKEND_URL}/agent`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(event),
      });

      if (!res.ok) {
        console.error("HTTP error:", res.status, res.statusText);
        setOutput(`[ERROR] Backend HTTP error: ${res.status}`);
        setLoading(false);
        return;
      }

      if (!res.body) {
        console.error("No response body");
        setOutput("[ERROR] Backend returned no data");
        setLoading(false);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      let text = "";
      let jsonText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        text += chunk;
        setOutput(text);
        jsonText += chunk;
      }

      // parse first JSON block for table
      const assessment = JSON.parse(jsonText.split("\n\n")[0]);

      const alert: Alert = {
        event_id,
        ip: "192.168.1.10",
        threat_type: assessment.threat_type,
        severity: assessment.severity,
        risk_score: assessment.risk_score,
        timestamp,
        explanation: assessment.explanation,
      };

      setHistory([alert, ...history]);
    } catch (err) {
      console.error("Fetch failed:", err);
      setOutput(`[ERROR] Fetch failed: ${err}`);
    }

    setLoading(false);
  };

  const severityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-600 text-white";
      case "high":
        return "bg-orange-500 text-white";
      case "medium":
        return "bg-yellow-400 text-black";
      case "low":
        return "bg-green-500 text-white";
      default:
        return "bg-gray-200 text-black";
    }
  };

  return (
    <div className="p-10 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">SOC Dashboard</h1>

      <button
        onClick={runAgent}
        className="px-6 py-3 bg-black text-white rounded hover:bg-gray-800 transition mb-6"
      >
        {loading ? "Analyzing..." : "Run Analysis"}
      </button>

      {/* Alerts Table */}
      <h2 className="text-2xl mb-4">Alerts History</h2>
      <table className="w-full border-collapse mb-6">
        <thead>
          <tr className="bg-gray-100">
            <th className="border px-4 py-2">Event ID</th>
            <th className="border px-4 py-2">IP</th>
            <th className="border px-4 py-2">Threat Type</th>
            <th className="border px-4 py-2">Severity</th>
            <th className="border px-4 py-2">Risk Score</th>
            <th className="border px-4 py-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {history.map((alert) => (
            <tr key={alert.event_id} className="hover:bg-gray-50">
              <td className="border px-4 py-2">{alert.event_id}</td>
              <td className="border px-4 py-2">{alert.ip}</td>
              <td className="border px-4 py-2">{alert.threat_type}</td>
              <td className={`border px-4 py-2 text-center ${severityColor(alert.severity)}`}>
                {alert.severity.toUpperCase()}
              </td>
              <td className="border px-4 py-2">{alert.risk_score.toFixed(2)}</td>
              <td className="border px-4 py-2">{alert.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Streaming Output */}
      <h2 className="text-2xl mb-2">Analysis Output</h2>
      <pre className="p-4 border rounded bg-gray-100 whitespace-pre-wrap">{output}</pre>
    </div>
  );
}
