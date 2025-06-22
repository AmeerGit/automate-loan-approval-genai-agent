import React, { useState } from "react";
import { Box, TextField, Button } from "@mui/material";
import WorkflowResultPanel from "./ResultPanel";

export default function LoanForm({ setWorkflowResult, setLog, setProgress }) {
  const [customerId, setCustomerId] = useState("");
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(false);
  const [workflowResult, setLocalWorkflowResult] = useState(null);

  // Demo/static values for appName, userId, sessionId
  const appName = "banking_rpa_agent";
  const userId = "u_123";
  const sessionId = "s_C125";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setLog([]);
    setProgress([]);
    setWorkflowResult(null);
    setLocalWorkflowResult(null);
    try {
      setLog(log => [...log, "Creating session..."]);
      // 1. Create session
      await fetch(`http://localhost:8000/apps/${appName}/users/${userId}/sessions/${sessionId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({})
      });
      setLog(log => [...log, "Session created. Submitting loan application..."]);
      setProgress(p => [...p, "Started loan workflow"]);
      // 2. Run workflow
      const res = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          appName,
          userId,
          sessionId,
          newMessage: {
            role: "user",
            parts: [{
              text: `Loan application amount is  ${amount} for customer ${customerId}.`,
            }],
          }
        })
      });
      const data = await res.json();
      setWorkflowResult(data);
      setLocalWorkflowResult(data);
      setProgress(p => [...p, "Workflow completed"]);
      setLog(log => [...log, "Workflow result received."]);
    } catch (err) {
      setLog(log => [...log, `Error: ${err}`]);
    }
    setLoading(false);
  };

  return (
    <>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: "flex", gap: 2, alignItems: "center" }}>
        <TextField
          label="Customer ID"
          value={customerId}
          onChange={e => setCustomerId(e.target.value)}
          required
        />
        <TextField
          label="Amount"
          type="number"
          value={amount}
          onChange={e => setAmount(e.target.value)}
          required
        />
        <Button type="submit" variant="contained" disabled={loading}>
          {loading ? "Processing..." : "Submit"}
        </Button>
      </Box>
      <WorkflowResultPanel result={workflowResult} />
    </>
  );
}
