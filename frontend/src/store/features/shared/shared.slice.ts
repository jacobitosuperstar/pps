import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { SharedState, sharedInitialState } from "./shared.init";

export const sharedSlice = createSlice({
  name: "shared",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState: sharedInitialState,
  reducers: {
    changeTitle: (state, action: PayloadAction<SharedState["title"]>) => {
      state.title = action.payload;
    },
    openDrawer: (state) => {
      state.drawer = true;
    },
    closeDrawer: (state) => {
      state.drawer = false;
    },
  },
});

export const { changeTitle, closeDrawer, openDrawer } = sharedSlice.actions;
