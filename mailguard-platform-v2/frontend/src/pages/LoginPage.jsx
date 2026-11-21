import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getErrorMessage } from "../api/apiClient";

// Faqja Login (/login)
function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { login, isLoading } = useAuthStore();

  // Pas kycjes me sukses perdoruesi dergohet te Dashboard
  const handleLogin = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (error) {
      setErrorMessage(getErrorMessage(error, "Login failed. Please try again."));
    }
  };

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="page-title text-center">Login</h1>

      <form onSubmit={handleLogin} className="card space-y-4">
        {errorMessage && <p className="alert-error">{errorMessage}</p>}

        <div>
          <label className="form-label">Email</label>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            className="input-field"
          />
        </div>

        <div>
          <label className="form-label">Password</label>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            className="input-field"
          />
        </div>

        <button type="submit" disabled={isLoading} className="btn-primary w-full">
          {isLoading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-muted-text text-center">
          No account?{" "}
          <Link to="/register" className="text-accent hover:underline">
            Register here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;
