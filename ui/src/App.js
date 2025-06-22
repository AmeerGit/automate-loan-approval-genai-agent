import React, { useState } from "react";
import { Container, Typography, Box, Paper, Tabs, Tab } from "@mui/material";
import TaskSelector from "./TaskSelector";
import LoanForm from "./LoanForm";
import WorkflowProgress from "./WorkflowProgress";
import ActionLog from "./ActionLog";
import ResultPanel from "./ResultPanel";

export default function App() {
  const [task, setTask] = useState("process_loan");
  const [workflowResult, setWorkflowResult] = useState(null);
  const [log, setLog] = useState([]);
  const [progress, setProgress] = useState([]);
  const [tab, setTab] = useState(0);

  const handleTaskChange = (newTask) => {
    console.log("Selected task:", newTask);
    setTask(newTask);
    setWorkflowResult(null);
    setProgress([]);
    setLog([]);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'start', mb: 4 }}>
               <img src="/caixabank-logo.svg" alt="Caixabank Logo" style={{ height: 48, marginRight: 20 }} />
               <Box>
                 <span style={{ fontSize: 28, fontWeight: 600, color: '#003366', display: 'block' }}>
                   CaixaFlow
                 </span>
                 <span style={{ fontSize: 16, fontWeight: 400, color: '#00B2A9', display: 'block' }}>
                   GenAI-Powered Banking RPA Back Office
                 </span>
               </Box>
             </Box>
      <Paper sx={{ p: 2, mb: 2 }}>
        <TaskSelector task={task} onChange={handleTaskChange} />
        {task === "process_loan" && (
          <LoanForm
            setWorkflowResult={setWorkflowResult}
            setLog={setLog}
            setProgress={setProgress}
          />
        )}
        {/* Add more forms for other tasks as needed */}
      </Paper>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)}>
          <Tab label="Workflow Progress" />
          <Tab label="Action Log" />
          <Tab label="Result" />
        </Tabs>
      </Box>
      {tab === 0 && <WorkflowProgress progress={progress} />}
      {tab === 1 && <ActionLog log={log} />}
      {tab === 2 && <ResultPanel result={workflowResult} />}
    </Container>
  );
}
