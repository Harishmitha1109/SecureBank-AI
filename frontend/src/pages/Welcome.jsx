import { Link } from "react-router-dom";
import "../styles/Welcome.css";

function Welcome() {
  return (
    <div className="welcome-container">
      <div className="card">
        <div className="logo">🛡️</div>
        <h1>SecureBank AI</h1>

      <h3>Continuous Behavioral Authentication</h3>

        <p>
  Experience next-generation banking secured by AI-driven behavioral biometrics and continuous authentication.
</p>

        <div className="buttons">

  <Link to="/login">
    <button className="primary-btn">
      Login
    </button>
  </Link>

  <Link to="/register">
    <button className="secondary-btn">
      Create Account
    </button>
  </Link>

</div>

        <div className="features">
          <div>🛡 AI Protection</div>
          <div>📊 Live Analytics</div>
          <div>🔒 Secure Banking</div>
        </div>
      </div>
    </div>
  );
}

export default Welcome;