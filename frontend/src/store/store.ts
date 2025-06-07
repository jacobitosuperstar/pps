import { configureStore } from "@reduxjs/toolkit";
import { useDispatch, useSelector } from "react-redux";
import type { TypedUseSelectorHook } from "react-redux";
import { authSlice, authPreloadState, authListener } from "./features/auth";
import { authApi } from "./apis/auth.api";
import { employeesApi } from "./apis/employees.api";
import { machinesApi } from "./apis/machines.api";
import { OOOApi } from "./apis/ooo.api";

export const store = configureStore({
  reducer: {
    [authSlice.name]: authSlice.reducer,
    //
    [authApi.reducerPath]: authApi.reducer,
    //
    [employeesApi.reducerPath]: employeesApi.reducer,
    //
    [machinesApi.reducerPath]: machinesApi.reducer,
    //
    [OOOApi.reducerPath]: OOOApi.reducer,
  },
  devTools: process.env.NODE_ENV !== "production",
  preloadedState: {
    auth: authPreloadState(),
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(authListener.middleware)
      .concat(authApi.middleware)
      .concat(employeesApi.middleware)
      .concat(machinesApi.middleware)
      .concat(OOOApi.middleware),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;
// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
