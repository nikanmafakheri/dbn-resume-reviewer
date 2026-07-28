import { useAuth } from '../../hooks/useAuth';
import { Button } from '../ui/Button';

export function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
      <h1 className="text-lg font-semibold text-gray-900">Resume Reviewer</h1>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">{user?.email}</span>
        <Button variant="secondary" onClick={logout}>
          Logout
        </Button>
      </div>
    </header>
  );
}
