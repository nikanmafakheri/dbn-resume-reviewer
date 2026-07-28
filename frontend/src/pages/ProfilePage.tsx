import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import { Alert } from '../components/ui/Alert';
import { updateMe } from '../api/users';

export function ProfilePage() {
  const { user, isLoading } = useAuth();
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);
    try {
      await updateMe({ full_name: fullName || undefined });
      setSuccess('Profile updated successfully');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to update profile';
      setError(msg);
    } finally {
      setSaving(false);
    }
  };

  if (isLoading || !user) return null;

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Profile</h1>

      <Card className="p-6">
        <div className="space-y-4">
          <Input label="Email" value={user.email} disabled />

          <div>
            <label className="block text-sm font-medium text-gray-700">Role</label>
            <p className="mt-1 text-sm text-gray-900 capitalize">{user.role}</p>
          </div>

          <Input
            label="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Your name"
          />

          {success && (
            <Alert variant="success" onDismiss={() => setSuccess(null)}>
              {success}
            </Alert>
          )}
          {error && (
            <Alert variant="error" onDismiss={() => setError(null)}>
              {error}
            </Alert>
          )}

          <div className="flex justify-end">
            <Button onClick={handleSave} loading={saving}>
              Save Changes
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
