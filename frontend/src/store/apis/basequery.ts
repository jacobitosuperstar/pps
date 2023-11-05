import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const appBaseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:3000/",
});
