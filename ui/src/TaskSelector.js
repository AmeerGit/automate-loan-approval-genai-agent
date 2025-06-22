import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

export default function TaskSelector({ task, onChange }) {
  return (
    <FormControl fullWidth sx={{ mb: 2 }}>
      <InputLabel>Task</InputLabel>
      <Select value={task} label="Task" onChange={e => onChange(e.target.value)}>
        <MenuItem value="process_loan">Process Loan Application</MenuItem>
        {/* Add more tasks as needed */}
      </Select>
    </FormControl>
  );
}
