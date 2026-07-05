import { Link } from "react-router-dom";
import useAuthStore from "../store/authStore";

function HomePage() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-white mb-3">MailGuard AI Platform</h1>
      <p className="text-lg text-slate-300 mb-10">
        Full-stack email scanning platform powered by Machine Learning
      </p>

      <div className="grid sm:grid-cols-3 gap-4 mb-10 text-left">
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-green-400 font-semibold mb-1">Safe</p>
          <p className="text-sm text-slate-400">
            Normal, legitimate emails that pose no risk.
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-yellow-400 font-semibold mb-1">Spam</p>
          <p className="text-sm text-slate-400">
            Unwanted bulk or promotional emails.
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-5">
          <p className="text-red-400 font-semibold mb-1">Phishing</p>
          <p className="text-sm text-slate-400">
            Malicious emails that try to steal your information.
          </p>
        </div>
      </div>

      <p className="text-slate-300 mb-8">
        Paste an email and our Machine Learning model tells you instantly if it
        is safe, spam, or a phishing attempt — with a confidence score. After
        logging in, every scan is saved so you can review your scan history at
        any time.
      </p>

      {isAuthenticated ? (
        <Link
          to="/dashboard"
          className="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded text-white font-medium"
        >
          Go to Dashboard
        </Link>
      ) : (
        <div className="flex justify-center gap-4">
          <Link
            to="/login"
            className="bg-slate-700 hover:bg-slate-600 px-6 py-3 rounded text-white font-medium"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="bg-emerald-600 hover:bg-emerald-500 px-6 py-3 rounded text-white font-medium"
          >
            Register
          </Link>
        </div>
      )}
    </div>
  );
}

export default HomePage;
