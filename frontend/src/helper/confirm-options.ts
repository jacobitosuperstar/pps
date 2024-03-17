import { ConfirmOptions } from "material-ui-confirm";

export const defaultConfirmOption = (optionsProps: ConfirmOptions) => {
  const options: ConfirmOptions = {
    ...optionsProps,
    confirmationText: "Confirmar",
    cancellationText: "Cancelar",
  };

  return options;
};
