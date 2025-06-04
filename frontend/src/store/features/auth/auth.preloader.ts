import { localstorageKeys } from "@/constant/localstorage-keys";
import { type AuthState, authInitialState } from "./auth.init";
import { createLocalStoragePreloader } from "@/helper/create-preloader";

export const authPreloadState = createLocalStoragePreloader<AuthState>(
  localstorageKeys.auth,
  authInitialState
);
