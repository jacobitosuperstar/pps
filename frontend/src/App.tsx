import { RouterProvider } from "react-router-dom";
import { router } from "./router";
import { Toaster } from "./components/ui/sonner";
import { Provider } from "react-redux";
import { store } from "./store/store";
import { ConfirmProvider } from "./components/providers/confirm-provider";

function App() {
  return (
    <>
      <Provider store={store}>
        <ConfirmProvider>
          <RouterProvider router={router} />
          <Toaster position="top-center" richColors />
        </ConfirmProvider>
      </Provider>
    </>
  );
}

export default App;
