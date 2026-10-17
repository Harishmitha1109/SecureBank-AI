import { Routes, Route } from "react-router-dom";

import Splash from "./pages/Splash";
import Welcome from "./pages/Welcome";
import Login from "./pages/Login";
import Register from "./pages/Register";

import Dashboard from "./pages/Dashboard";
import Transfer from "./pages/Transfer";
import Transactions from "./pages/Transactions";
import Cards from "./pages/Cards";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import Deposit from "./pages/Deposit";
function App() {

  return (

    <Routes>

      <Route path="/" element={<Splash />} />

      <Route path="/welcome" element={<Welcome />} />

      <Route path="/login" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route path="/dashboard" element={<Dashboard />} />

      <Route path="/transfer" element={<Transfer />} />
      <Route path="/deposit" element={<Deposit />} />

      <Route path="/transactions" element={<Transactions />} />

      <Route path="/cards" element={<Cards />} />

      <Route path="/profile" element={<Profile />} />

      <Route path="/settings" element={<Settings />} />

    </Routes>

  );

}

export default App;