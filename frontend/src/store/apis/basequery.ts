import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { RootState } from "../store";
// import Cookies from "js-cookie";

export const appBaseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:8000/",
  // credentials: "include",
  prepareHeaders: (headers, context) => {
    const state = context.getState() as RootState;
    const token = state.auth.token;

    headers.set("Authorization", "Token " + token);

    return headers;
  },
});
