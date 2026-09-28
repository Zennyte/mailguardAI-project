import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

// Forma e kyçjes
function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login, loading } = useAuthStore();

  // Dergon email+fjalekalim dhe ridrejton te dashboard nese ka sukses
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === "string" ? detail : "Login failed. Please try again.");
    }
  };

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="page-title text-center text-2xl">Login</h1>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <p className="alert-error">{error}</p>}

        <div>
          <label className="form-label">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input-field"
          />
        </div>

        <div>
          <label className="form-label">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="input-field"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-[var(--text-dim)] text-center">
          No account?{" "}
          <Link to="/register" className="text-[var(--accent)] hover:underline">
            Register here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;
