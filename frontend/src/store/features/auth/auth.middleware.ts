import { createListenerMiddleware } from "@reduxjs/toolkit";
import { loginUser, logoutUser } from "./auth.slice";
import { localstorageKeys } from "@/constants";
import { RootState } from "@/store/store";

const authListener = createListenerMiddleware();

authListener.startListening({
  actionCreator: loginUser,
  effect: async (action, listenerApi) => {
    // Can cancel other running instances
    listenerApi.cancelActiveListeners();

    const { auth } = listenerApi.getState() as RootState;

    localStorage.setItem(localstorageKeys.auth, JSON.stringify(auth));
  },
});

authListener.startListening({
  actionCreator: logoutUser,
  effect: (_action, listenerApi) => {
    // Can cancel other running instances
    listenerApi.cancelActiveListeners();

    localStorage.removeItem(localstorageKeys.auth);
  },
});

export { authListener };
