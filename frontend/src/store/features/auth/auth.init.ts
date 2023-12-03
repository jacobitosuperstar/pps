export interface AuthState {
  isAuthenticate: boolean;
  token: string | null;
}

export const authInitialState: AuthState = {
  isAuthenticate: false,
  token: null,
};
