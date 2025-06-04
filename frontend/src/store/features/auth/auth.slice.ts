import { type PayloadAction, createSlice } from "@reduxjs/toolkit";
import { authInitialState } from "./auth.init";

interface LoginUserPayload {
  token: string;
  user: {
    identification: string;
    names: string;
    last_names: string;
    role: string;
    birthday: string | null;
  };
}

export const authSlice = createSlice({
  name: "auth",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState: authInitialState,
  reducers: {
    loginUser: (state, action: PayloadAction<LoginUserPayload>) => {
      state.isAuthenticate = true;
      state.token = action.payload.token;
      state.user = action.payload.user;
    },
    logoutUser: (state) => {
      state.isAuthenticate = false;
      state.token = null;
      state.user = null;
    },
  },
});

export const { loginUser, logoutUser } = authSlice.actions;
