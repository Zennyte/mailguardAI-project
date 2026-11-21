import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import useAuthStore from "../store/authStore";
import { getErrorMessage } from "../api/apiClient";

// Faqja Register (/register)
function RegisterPage() {
  // Emrat e fushave jane te njejte me ata qe pret backend-i (POST /auth/register)
  const [registrationForm, setRegistrationForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { register, isLoading } = useAuthStore();

  // Nje funksion per te gjitha fushat: atributi "name" i input-it tregon cilen fushe te ndryshoje
  const handleFieldChange = (event) => {
    setRegistrationForm({ ...registrationForm, [event.target.name]: event.target.value });
  };

  // Pas regjistrimit perdoruesi kycet automatikisht dhe dergohet te Dashboard
  const handleRegister = async (event) => {
    event.preventDefault();
    setErrorMessage("");
    try {
      await register(registrationForm);
      navigate("/dashboard");
    } catch (error) {
      setErrorMessage(
        getErrorMessage(error, "Registration failed. Password must be at least 8 characters."),
      );
    }
  };

  return (
    <div className="max-w-sm mx-auto">
      <h1 className="page-title text-center">Register</h1>

      <form onSubmit={handleRegister} className="card space-y-4">
        {errorMessage && <p className="alert-error">{errorMessage}</p>}

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="form-label">First name</label>
            <input
              name="first_name"
              value={registrationForm.first_name}
              onChange={handleFieldChange}
              required
              className="input-field"
            />
          </div>
          <div>
            <label className="form-label">Last name</label>
            <input
              name="last_name"
              value={registrationForm.last_name}
              onChange={handleFieldChange}
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
            value={registrationForm.email}
            onChange={handleFieldChange}
            required
            className="input-field"
          />
        </div>

        <div>
          <label className="form-label">Password</label>
          <input
            type="password"
            name="password"
            value={registrationForm.password}
            onChange={handleFieldChange}
            required
            minLength={8}
            className="input-field"
          />
        </div>

        <button type="submit" disabled={isLoading} className="btn-primary w-full">
          {isLoading ? "Creating account..." : "Register"}
        </button>

        <p className="text-sm text-muted-text text-center">
          Already have an account?{" "}
          <Link to="/login" className="text-accent hover:underline">
            Login here
          </Link>
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;
