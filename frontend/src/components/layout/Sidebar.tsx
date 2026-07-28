import { NavLink } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const links = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/upload', label: 'Upload Resume', icon: '📤' },
  { to: '/profile', label: 'Profile', icon: '👤' },
];

export function Sidebar() {
  const { user } = useAuth();
  const isRecruiter = user?.role === 'recruiter' || user?.role === 'admin';

  return (
    <aside className="flex w-64 flex-col border-r border-gray-200 bg-white">
      <div className="flex h-16 items-center gap-2 border-b border-gray-200 px-6">
        <span className="text-xl">📋</span>
        <span className="text-lg font-bold text-gray-900">DBN Resume</span>
      </div>
      <nav className="flex-1 space-y-1 p-4">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <span>{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
        {isRecruiter && (
          <NavLink
            to="/standards"
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            <span>📏</span>
            Standards
          </NavLink>
        )}
      </nav>
    </aside>
  );
}
