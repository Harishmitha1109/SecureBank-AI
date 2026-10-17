import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles/Login.css";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {

    try {

      const response = await fetch("http://127.0.0.1:5000/login", {

        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          email,
          password,
        }),

      });

      const data = await response.json();

      alert(data.message);

      if (data.success) {

        // Save logged-in user
        localStorage.setItem(
          "user",
          JSON.stringify({
            name: data.name,
            email: data.email,
          })
        );

        navigate("/dashboard");

      }

    } catch (error) {

      console.error(error);
      alert("Server Error");

    }

  };

  return (

    <div className="login-container">

      <div className="login-card">

        <div className="logo">🛡️</div>

        <h1>SecureBank AI</h1>

        <h3>Welcome Back</h3>

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={handleLogin}>
          Login
        </button>

        <p className="register">
          Don't have an account?{" "}
          <Link to="/register">Register</Link>
        </p>

      </div>

    </div>

  );

}

export default Login;