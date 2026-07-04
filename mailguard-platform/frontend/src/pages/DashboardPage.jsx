import useAuthStore from "../store/authStore";

function DashboardPage() {
  const user = useAuthStore((state) => state.user);

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-2">Dashboard</h1>
      {user && (
        <p className="text-slate-300 mb-6">
          Welcome, {user.first_name} {user.last_name}!
        </p>
      )}
      <div className="bg-slate-800 rounded-lg p-6 text-slate-400">
        Scanner and statistics will be added in the next commits.
      </div>
    </div>
  );
}

export default DashboardPage;
