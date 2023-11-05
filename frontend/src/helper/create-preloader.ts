import { compareObjectKeys } from "./compare-object-keys";

export const createLocalStoragePreloader =
  <T>(key: string, initialState: T) =>
  (): T => {
    const stringifyAuth = localStorage.getItem(key);

    if (!stringifyAuth) {
      return initialState;
    }

    const auth = JSON.parse(stringifyAuth);

    const isValid = compareObjectKeys(initialState, auth);

    if (!isValid) {
      return initialState;
    }

    return auth as T;
  };
