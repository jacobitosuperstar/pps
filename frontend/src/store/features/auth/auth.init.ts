export interface AuthState {
  isAuthenticate: boolean;
  token: string | null;
  remenberedId: string;
}

export const authInitialState: AuthState = {
  isAuthenticate: false,
  token: null,
  remenberedId: "",
};
