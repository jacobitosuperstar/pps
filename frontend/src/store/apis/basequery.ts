import { fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import Cookies from "js-cookie";

export const appBaseQuery = fetchBaseQuery({
  baseUrl: "http://localhost:8000/",
  // credentials: "include",
  prepareHeaders: (headers, context) => {
    if (context.endpoint === "pin") return headers;

    // Retrieve the CSRF token from the cookie
    const csrfToken = Cookies.get("csrftoken");
    // Set the CSRF token in the headers
    headers.set("X-CSRFTOKEN", csrfToken || "");
    headers.set("Content-type", "application/json");

    return headers;
  },
});
