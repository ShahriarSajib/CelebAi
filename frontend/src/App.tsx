import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import ResetPassword from "./pages/ResetPassword";
import Login from "./pages/Login";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/reset-password"
          element={<ResetPassword />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;