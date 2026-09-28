import { useEffect, useState } from "react";

import useAuthStore from "../store/authStore";
import { getNotifications, markAsRead } from "../services/notificationService";
import { connectNotifications } from "../services/websocketService";

// Kambana e njoftimeve - lidhet me WebSocket per njoftime live
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

  // Shenon nje njoftim si te lexuar
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
        className="relative flex items-center justify-center w-9 h-9 border border-[var(--border)]
          rounded text-[var(--text-dim)] hover:bg-[var(--surface-2)]"
        title="Notifications"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
          strokeLinecap="round" strokeLinejoin="round" className="w-4.5 h-4.5">
          <path d="M6 8a6 6 0 0 1 12 0c0 4 1.5 5.5 2 6.5H4c.5-1 2-2.5 2-6.5Z" />
          <path d="M10 19a2 2 0 0 0 4 0" />
        </svg>
        {unreadCount > 0 && (
          <span
            className="absolute -top-1.5 -right-1.5 bg-[var(--danger)] text-[#1a0505] text-[10px]
              leading-none font-bold rounded-full w-4 h-4 flex items-center justify-center"
          >
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-80 bg-[var(--surface)] border border-[var(--border)] rounded shadow-lg z-30">
          <p className="px-4 py-2 text-xs uppercase tracking-wide text-[var(--text-dim)] border-b border-[var(--border)]">
            Notifications
          </p>
          {notifications.length === 0 ? (
            <p className="px-4 py-3 text-sm text-[var(--text-faint)]">No notifications yet.</p>
          ) : (
            <ul className="max-h-72 overflow-y-auto">
              {notifications.map((n) => (
                <li
                  key={n.id}
                  className={`px-4 py-2 border-b border-[var(--border)] text-sm ${
                    n.is_read ? "text-[var(--text-faint)]" : "text-[var(--text)]"
                  }`}
                >
                  <p className="font-medium">{n.title}</p>
                  <p className="text-xs text-[var(--text-dim)]">{n.message}</p>
                  {!n.is_read && (
                    <button
                      onClick={() => handleMarkRead(n.id)}
                      className="text-xs text-[var(--accent)] hover:underline mt-1"
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
