import { IconButton, TableCell, TableRow, Typography } from "@mui/material";
import { FC, ReactElement } from "react";

interface Props {
  message: string;
  colSpan: number;
  icon: ReactElement;
}

const CellTableMessage: FC<Props> = ({ colSpan, icon, message }) => {
  return (
    <TableRow>
      <TableCell align="center" colSpan={colSpan}>
        <IconButton disabled>{icon}</IconButton>
        <Typography variant="body2" color="textSecondary">
          {message}
        </Typography>
      </TableCell>
    </TableRow>
  );
};

export default CellTableMessage;
