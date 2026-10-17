import { NavLink } from "react-router-dom";
import "./Sidebar.css";

function Sidebar() {

  return (

    <div className="sidebar">

      <h2 className="logo">🏦 SecureBank AI</h2>

      <NavLink to="/dashboard" className="menu">
        🏠 Dashboard
      </NavLink>

      <NavLink to="/transfer" className="menu">
        💸 Transfer
      </NavLink>

      <NavLink to="/deposit" className="menu">
        💰 Deposit
      </NavLink>

      <NavLink to="/transactions" className="menu">
        📜 Transactions
      </NavLink>

      <NavLink to="/cards" className="menu">
        💳 Cards
      </NavLink>

      <NavLink to="/profile" className="menu">
        👤 Profile
      </NavLink>

      <NavLink to="/settings" className="menu">
        ⚙️ Settings
      </NavLink>

    </div>

  );

}

export default Sidebar;