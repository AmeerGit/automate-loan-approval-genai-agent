import React from "react";
import { List, ListItem, ListItemText } from "@mui/material";

export default function ActionLog({ log }) {
  return (
    <List>
      {log.map((entry, i) => (
        <ListItem key={i}>
          <ListItemText primary={entry} />
        </ListItem>
      ))}
    </List>
  );
}
