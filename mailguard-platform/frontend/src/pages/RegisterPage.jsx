import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";

function RegisterPage() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { register, loading } = useAuthStore();

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      await register(form);
      navigate("/dashboard");
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(
        typeof detail === "string"
          ? detail
          : "Registration failed. Password must be at least 8 characters.",
      );
    }
  };

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="text-2xl font-bold text-white mb-6 text-center">Register</h1>

      <form onSubmit={handleSubmit} className="bg-slate-800 rounded-lg p-6 space-y-4">
        {error && (
          <p className="bg-red-900/50 text-red-300 text-sm rounded px-3 py-2">{error}</p>
        )}

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm text-slate-300 mb-1">First name</label>
            <input
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              required
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-300 mb-1">Last name</label>
            <input
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              required
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-1">Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <div>
          <label className="block text-sm text-slate-300 mb-1">Password</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            minLength={8}
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 py-2 rounded text-white font-medium"
        >
          {loading ? "Creating account..." : "Register"}
        </button>

        <p className="text-sm text-slate-400 text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-emerald-400 hover:underline">
            Login here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;
