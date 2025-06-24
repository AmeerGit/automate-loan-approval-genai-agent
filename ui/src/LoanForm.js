import React, { useState } from "react";
import { Box, TextField, Button, Typography, Paper } from "@mui/material";
import CircularProgress from '@mui/material/CircularProgress';
import WorkflowResultPanel from "./ResultPanel";

export default function LoanForm({ setWorkflowResult, setLog, setProgress }) {
  const [customerId, setCustomerId] = useState("");
  const [amount, setAmount] = useState("");
  const [loading, setLoading] = useState(false);
  const [workflowResult, setLocalWorkflowResult] = useState(null);
  const [showEscalation, setShowEscalation] = useState(false);
  const [escalationReason, setEscalationReason] = useState("");
  const [humanDecision, setHumanDecision] = useState({ status: "approved_by_human", notes: "" });

  // Demo/static values for appName, userId, sessionId
  const appName = "banking_rpa_agent";
  const userId = "u_123";
  const sessionId = "s_C126";

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
      // Check for escalation in result (handle ADK event array)
      let loanResult = null;
      let autoRejectReason = null;
      if (Array.isArray(data)) {
        // Find the functionResponse part
        const workflowStep = data.find(r => r.content?.parts?.[0]?.functionResponse);
        if (workflowStep) {
          loanResult = workflowStep.content.parts[0].functionResponse.response.loan_result;
        }
      } else {
        loanResult = data?.loan_result;
      }
      // Handle auto-reject (salary below threshold)
      if (loanResult?.status === "rejected" && loanResult?.reason?.toLowerCase().includes("salary below minimum")) {
        setWorkflowResult(data);
        setLocalWorkflowResult(data);
        setProgress(p => [...p, "Application auto-rejected"]);
        setLog(log => [...log, "Application rejected: " + loanResult.reason]);
        setShowEscalation(false);
        setLoading(false);
        return;
      }
      // Handle escalation for borderline salary (risk review)
      if (loanResult?.status === "pending" && loanResult?.escalation_result?.escalation === "pending_human" && loanResult?.reason?.toLowerCase().includes("salary in borderline")) {
        setEscalationReason(
          `Risk Analyst Review Required\nReason: ${loanResult.escalation_result.reason}\n` +
          (loanResult.escalation_result.context?.customer ? `Customer: ${loanResult.escalation_result.context.customer.name} (KYC: ${loanResult.escalation_result.context.customer.kyc_status}, Credit: ${loanResult.escalation_result.context.customer.credit_score})\n` : "") +
          (loanResult.escalation_result.context?.application ? `Amount: ${loanResult.escalation_result.context.application.amount}` : "")
        );
        setShowEscalation(true);
        setLocalWorkflowResult(data);
        setWorkflowResult(data);
        setLoading(false);
        return;
      }
      setWorkflowResult(data);
      setLocalWorkflowResult(data);
      setProgress(p => [...p, "Workflow completed"]);
      setLog(log => [...log, "Workflow result received."]);
    } catch (err) {
      setLog(log => [...log, `Error: ${err}`]);
    }
    setLoading(false);
  };

  // Handler for human-in-the-loop approval
  const handleHumanDecision = async (decision) => {
    setShowEscalation(false);
    setLoading(true);
    setLog(log => [...log, `Submitting human decision: ${decision.status}`]);
    // Re-run workflow, passing the human decision within the prompt
    // so the agent's LLM can parse it and pass it to the tool.
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
            text: `The loan application for customer ${customerId} for amount ${amount} requires a manual decision. Please process the following human decision: status is '${decision.status}', notes are '${decision.notes}'.`,
          }]
        },
      })
    });
    const data = await res.json();
    setWorkflowResult(data);
    setLocalWorkflowResult(data);
    setProgress(p => [...p, "Workflow completed (human)"]);
    setLog(log => [...log, "Workflow result received (human)."]);
    setLoading(false);
  };

  return (
    <>
      {/* Header with logo and app/hackathon name, before the form/task dropdown */}
      {/* ...existing header code... */}
      <Box sx={{ position: 'relative' }}>
        {/* Loader overlay when loading */}
        {loading && (
          <Box sx={{
            position: 'absolute',
            top: 0, left: 0, width: '100%', height: '100%',
            bgcolor: 'rgba(255,255,255,0.7)',
            zIndex: 10,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <CircularProgress size={60} color="primary" />
          </Box>
        )}
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
        {/* Escalation section (in-page, not modal) */}
        {showEscalation && (
          <Paper elevation={4} sx={{ mt: 4, p: 3, bgcolor: '#fffbe6', border: '1px solid #ffe082' }}>
            <Typography variant="h6" color="warning.main" gutterBottom>
              Human Approval Required
            </Typography>
            <Typography variant="body2" sx={{ whiteSpace: 'pre-line', mb: 2 }}>{escalationReason}</Typography>
            <TextField
              label="Notes (required)"
              value={humanDecision.notes}
              onChange={e => setHumanDecision({ ...humanDecision, notes: e.target.value })}
              fullWidth
              multiline
              sx={{ mt: 2 }}
              required
              error={!humanDecision.notes}
              helperText={!humanDecision.notes ? "Please provide notes for audit." : ""}
            />
            <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
              <Button onClick={() => handleHumanDecision({ status: "rejected_by_human", notes: humanDecision.notes })} color="error" disabled={!humanDecision.notes} variant="outlined">Reject</Button>
              <Button onClick={() => handleHumanDecision({ status: "approved_by_human", notes: humanDecision.notes })} color="primary" variant="contained" disabled={!humanDecision.notes}>Approve</Button>
            </Box>
          </Paper>
        )}
        <WorkflowResultPanel result={workflowResult} />
      </Box>
    </>
  );
}
