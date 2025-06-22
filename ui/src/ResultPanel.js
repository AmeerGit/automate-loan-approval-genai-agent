import React from "react";
import { Paper, Typography, Box, Divider, Chip } from "@mui/material";

export default function ResultPanel({ result }) {
  if (!result) return <Typography variant="body1">No result yet.</Typography>;
  // Try to extract key workflow info if result is an array
  let workflowStep, summaryStep, loanResult, customer, compliance, rpaLog, summaryText;
  if (Array.isArray(result)) {
    workflowStep = result.find(r => r.content?.parts?.[0]?.functionResponse);
    summaryStep = result.find(r => r.content?.parts?.[0]?.text);
    if (workflowStep) {
      const resp = workflowStep.content.parts[0].functionResponse.response;
      loanResult = resp.loan_result;
      customer = resp.customer;
      compliance = resp.compliance;
      rpaLog = loanResult?.rpa_log;
    }
    if (summaryStep) {
      summaryText = summaryStep.content.parts[0].text;
    }
  }
  return (
    <Paper sx={{ p: 2, mt: 2 }}>
      <Typography variant="h6">Workflow Result</Typography>
      {loanResult && (
        <Box mb={2}>
          <Typography variant="subtitle1">
            Status: <Chip label={loanResult.status} color={loanResult.status === "approved" ? "success" : "error"} />
          </Typography>
          <Typography variant="body1">{loanResult.message}</Typography>
        </Box>
      )}
      {customer && (
        <Box mb={2}>
          <Typography variant="subtitle2">Customer</Typography>
          <Typography variant="body2">{customer.name} (ID: {customer.customer_id})</Typography>
          <Typography variant="body2">KYC: {customer.kyc_status}, Credit Score: {customer.credit_score}</Typography>
          <Typography variant="body2">Account: {customer.account_status}, Income: ${customer.annual_income}</Typography>
        </Box>
      )}
      {compliance && (
        <Box mb={2}>
          <Typography variant="subtitle2">Compliance</Typography>
          <Typography variant="body2" color={compliance.compliant ? "success.main" : "error.main"}>
            {compliance.compliant ? "Compliant" : "Non-compliant"}
          </Typography>
        </Box>
      )}
      {rpaLog && (
        <Box mb={2}>
          <Typography variant="subtitle2">RPA Action Log</Typography>
          <Typography variant="body2">Action: {rpaLog.action}</Typography>
          <Typography variant="body2">Status: {rpaLog.status}</Typography>
          <Typography variant="body2">Timestamp: {new Date(rpaLog.timestamp * 1000).toLocaleString()}</Typography>
        </Box>
      )}
      {summaryText && (
        <Box mb={2}>
          <Divider />
          <Typography variant="body1" sx={{ mt: 1 }}>{summaryText}</Typography>
        </Box>
      )}
      {/* Fallback: show raw JSON if nothing parsed */}
      {!loanResult && !customer && !compliance && !rpaLog && !summaryText && (
        <pre style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </Paper>
  );
}
