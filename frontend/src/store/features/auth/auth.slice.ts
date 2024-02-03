import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { authInitialState } from "./auth.init";

interface LoginUserPayload {
  token: string;
  remenberedId: string;
}

export const authSlice = createSlice({
  name: "auth",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState: authInitialState,
  reducers: {
    loginUser: (state, action: PayloadAction<LoginUserPayload>) => {
      state.isAuthenticate = true;
      state.token = action.payload.token;
      state.remenberedId = action.payload.remenberedId;
    },
    logoutUser: (state) => {
      state.isAuthenticate = false;
      state.token = null;
    },
  },
});

export const { loginUser, logoutUser } = authSlice.actions;
