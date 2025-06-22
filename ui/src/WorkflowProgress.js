import React from "react";
import { List, ListItem, ListItemText } from "@mui/material";

export default function WorkflowProgress({ progress }) {
  return (
    <List>
      {progress.map((step, i) => (
        <ListItem key={i}>
          <ListItemText primary={step} />
        </ListItem>
      ))}
    </List>
  );
}
