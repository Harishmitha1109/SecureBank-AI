import Sidebar from "./Sidebar";
import BehaviorTracker from "../components/BehaviorTracker";
import "./MainLayout.css";

import { useState } from "react";
import { useNavigate } from "react-router-dom";

function MainLayout({ children }) {

  const user = JSON.parse(localStorage.getItem("user"));

  const navigate = useNavigate();

  const [showMenu, setShowMenu] = useState(false);

  const handleLogout = () => {

    localStorage.removeItem("user");

    navigate("/login");

  };

  return (

    <div className="layout">

      <BehaviorTracker email={user?.email} />

      <Sidebar />

      <div className="main-content">

        <div className="topbar">

          <div>

            <h2>🏦 SecureBank AI</h2>

            <p>AI Powered Behavioral Banking</p>

          </div>

          <div className="profile-menu">

            <div
              className="user-info"
              onClick={() => setShowMenu(!showMenu)}
            >
              👤 {user?.name} ▼
            </div>

            {showMenu && (

              <div className="dropdown-menu">

                <div onClick={() => navigate("/profile")}>
                  👤 My Profile
                </div>

                <div onClick={() => navigate("/settings")}>
                  ⚙️ Settings
                </div>

                <div onClick={handleLogout}>
                  🚪 Logout
                </div>

              </div>

            )}

          </div>

        </div>

        <div className="page-content">

          {children}

        </div>

      </div>

    </div>

  );

}

export default MainLayout;