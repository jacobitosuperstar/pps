import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { authInitialState } from "./auth.init";

export const authSlice = createSlice({
  name: "auth",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState: authInitialState,
  reducers: {
    loginUser: (state, action: PayloadAction<string>) => {
      state.isAuthenticate = true;
      state.token = action.payload;
    },
    logoutUser: (state) => {
      state.isAuthenticate = false;
      state.token = null;
    },
  },
});

export const { loginUser, logoutUser } = authSlice.actions;
