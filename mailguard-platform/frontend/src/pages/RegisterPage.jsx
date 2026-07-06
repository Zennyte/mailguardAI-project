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
      <h1 className="page-title text-center text-2xl">Register</h1>

      <form onSubmit={handleSubmit} className="card space-y-4">
        {error && <p className="alert-error">{error}</p>}

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="form-label">First name</label>
            <input
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              required
              className="input-field"
            />
          </div>
          <div>
            <label className="form-label">Last name</label>
            <input
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              required
              className="input-field"
            />
          </div>
        </div>

        <div>
          <label className="form-label">Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            className="input-field"
          />
        </div>

        <div>
          <label className="form-label">Password</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            minLength={8}
            className="input-field"
          />
        </div>

        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading ? "Creating account..." : "Register"}
        </button>

        <p className="text-sm text-[var(--text-dim)] text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-[var(--accent)] hover:underline">
            Login here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;
