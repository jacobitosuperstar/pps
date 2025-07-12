export interface AuthState {
  isAuthenticate: boolean;
  token: string | null;
  user: {
    identification: string;
    names: string;
    last_names: string;
    role: string;
    birthday: string | null;
  } | null;
}

export const authInitialState: AuthState = {
  isAuthenticate: false,
  token: null,
  user: null,
};
