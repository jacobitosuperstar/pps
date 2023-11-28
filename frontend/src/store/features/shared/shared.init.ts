export interface SharedState {
  drawer: boolean;
  title: "Dashboard" | "Personal" | "Programación" | "Produción";
}

export const sharedInitialState: SharedState = {
  drawer: false,
  title: "Dashboard",
};
