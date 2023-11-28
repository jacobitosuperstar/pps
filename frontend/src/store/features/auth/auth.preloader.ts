import { localstorageKeys } from "@/constants";
import { AuthState, authInitialState } from "./auth.init";
import { createLocalStoragePreloader } from "@/helper";

export const authPreloadState = createLocalStoragePreloader<AuthState>(
  localstorageKeys.auth,
  authInitialState
);
