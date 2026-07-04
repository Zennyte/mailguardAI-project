import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login, loading } = useAuthStore();

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
      <h1 className="text-2xl font-bold text-white mb-6 text-center">Login</h1>

      <form onSubmit={handleSubmit} className="bg-slate-800 rounded-lg p-6 space-y-4">
        {error && (
          <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2">{error}</p>
        )}

        <div>
          <label className="block text-sm text-slate-300 mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 py-2 rounded text-white font-medium"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-slate-400 text-center">
          No account?{" "}
          <Link to="/register" className="text-emerald-400 hover:underline">
            Register here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;
