import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { authInitialState } from "./auth.init";

export const authSlice = createSlice({
  name: "auth",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState: authInitialState,
  reducers: {
    loginUser: (state, action: PayloadAction<number>) => {
      state.isAuthenticate = true;
    },
    logoutUser: (state) => {
      state.isAuthenticate = false;
    },
  },
});

export const { loginUser, logoutUser } = authSlice.actions;
