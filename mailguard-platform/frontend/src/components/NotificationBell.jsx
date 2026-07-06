import { useEffect, useState } from "react";

import useAuthStore from "../store/authStore";
import { getNotifications, markAsRead } from "../services/notificationService";
import { connectNotifications } from "../services/websocketService";

function NotificationBell() {
  const user = useAuthStore((state) => state.user);
  const [notifications, setNotifications] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!user) return;

    getNotifications().then(setNotifications).catch(() => {});

    // Njoftimet e reja vijne live nga WebSocket
    const socket = connectNotifications(user.id, (notification) => {
      setNotifications((current) => [{ ...notification, is_read: false }, ...current]);
    });

    return () => socket.close();
  }, [user]);

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  const handleMarkRead = async (id) => {
    await markAsRead(id).catch(() => {});
    setNotifications((current) =>
      current.map((n) => (n.id === id ? { ...n, is_read: true } : n)),
    );
  };

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="relative bg-slate-700 hover:bg-slate-600 px-3 py-1.5 rounded-md transition-colors"
        title="Notifications"
      >
        🔔
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1.5">
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-80 bg-slate-800 border border-slate-700 rounded-xl shadow-xl z-30">
          <p className="px-4 py-2 text-sm font-semibold border-b border-slate-700">
            Notifications
          </p>
          {notifications.length === 0 ? (
            <p className="px-4 py-3 text-sm text-slate-400">No notifications yet.</p>
          ) : (
            <ul className="max-h-72 overflow-y-auto">
              {notifications.map((n) => (
                <li
                  key={n.id}
                  className={`px-4 py-2 border-b border-slate-700/50 text-sm ${
                    n.is_read ? "text-slate-500" : "text-slate-200"
                  }`}
                >
                  <p className="font-medium">{n.title}</p>
                  <p className="text-xs">{n.message}</p>
                  {!n.is_read && (
                    <button
                      onClick={() => handleMarkRead(n.id)}
                      className="text-xs text-emerald-400 hover:underline mt-1"
                    >
                      Mark as read
                    </button>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default NotificationBell;
