import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { type RootState } from "../store";

export const appBaseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:8000/api/",
  prepareHeaders: (headers, context) => {
    const state = context.getState() as RootState;
    const token = state.auth.token;

    headers.set("Authorization", "Token " + token);

    return headers;
  },
});
