import { useEffect, useState } from "react";

import useAuthStore from "../store/authStore";
import {
  getNotifications, markNotificationAsRead, openNotificationSocket,
} from "../api/notificationApi";

// Kambana e njoftimeve lart djathtas (pas kycjes).
// Rrethi i kuq tregon sa njoftime jane te palexuara; klikimi hap listen.
function NotificationBell() {
  const user = useAuthStore((state) => state.user);
  const [notifications, setNotifications] = useState([]);
  const [isListOpen, setIsListOpen] = useState(false);

  useEffect(() => {
    if (!user) return;

    // Njoftimet e vjetra vijne nga databaza...
    getNotifications().then(setNotifications).catch(() => {});

    // ...ndersa te rejat vijne live nga WebSocket dhe shtohen ne krye te listes
    const socket = openNotificationSocket((newNotification) => {
      setNotifications((currentNotifications) => [newNotification, ...currentNotifications]);
    });

    return () => socket.close();
  }, [user]);

  const unreadCount = notifications.filter((notification) => !notification.is_read).length;

  const handleMarkAsRead = async (notificationId) => {
    await markNotificationAsRead(notificationId).catch(() => {});
    setNotifications((currentNotifications) =>
      currentNotifications.map((notification) =>
        notification.id === notificationId ? { ...notification, is_read: true } : notification,
      ),
    );
  };

  return (
    <div className="relative">
      {/* Butoni i kambanes */}
      <button
        onClick={() => setIsListOpen(!isListOpen)}
        className="relative flex items-center justify-center w-9 h-9 border border-divider rounded-full text-muted-text hover:bg-raised-background"
        title="Notifications"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
          strokeLinecap="round" strokeLinejoin="round" className="w-4.5 h-4.5">
          <path d="M6 8a6 6 0 0 1 12 0c0 4 1.5 5.5 2 6.5H4c.5-1 2-2.5 2-6.5Z" />
          <path d="M10 19a2 2 0 0 0 4 0" />
        </svg>
        {unreadCount > 0 && (
          <span className="absolute -top-1.5 -right-1.5 bg-phishing text-white text-[10px] leading-none font-bold rounded-full w-4 h-4 flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {/* Lista qe hapet poshte kambanes */}
      {isListOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-card-background border border-divider rounded-2xl shadow-lg overflow-hidden z-30">
          <p className="px-4 py-2 text-xs uppercase tracking-wide text-muted-text border-b border-divider">
            Notifications
          </p>
          {notifications.length === 0 ? (
            <p className="px-4 py-3 text-sm text-faint-text">No notifications yet.</p>
          ) : (
            <ul className="max-h-72 overflow-y-auto">
              {notifications.map((notification) => (
                <li
                  key={notification.id}
                  className={`px-4 py-2 border-b border-divider text-sm ${
                    notification.is_read ? "text-faint-text" : "text-main-text"
                  }`}
                >
                  <p className="font-medium">{notification.title}</p>
                  <p className="text-xs text-muted-text">{notification.message}</p>
                  {!notification.is_read && (
                    <button
                      onClick={() => handleMarkAsRead(notification.id)}
                      className="text-xs text-accent hover:underline mt-1"
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
