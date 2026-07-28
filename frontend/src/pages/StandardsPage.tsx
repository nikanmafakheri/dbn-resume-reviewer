import { useState, useEffect } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Spinner } from '../components/ui/Spinner';
import { ErrorState } from '../components/ui/ErrorState';
import { EmptyState } from '../components/ui/EmptyState';
import type { StandardResponse } from '../types';
import * as standardsApi from '../api/dbnStandards';

export function StandardsPage() {
  const [standard, setStandard] = useState<StandardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState('');
  const [version, setVersion] = useState('');
  const [creating, setCreating] = useState(false);

  const fetchStandard = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { data } = await standardsApi.getActiveStandard();
      setStandard(data);
    } catch {
      setStandard(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStandard();
  }, []);

  const handleCreate = async () => {
    setCreating(true);
    try {
      const { data } = await standardsApi.createStandard({ name, version });
      setStandard(data);
      setShowCreate(false);
      setName('');
      setVersion('');
    } catch {
      setError('Failed to create standard');
    } finally {
      setCreating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Spinner className="h-8 w-8" />
      </div>
    );
  }

  if (error) return <ErrorState message={error} onRetry={fetchStandard} />;

  if (!standard && !showCreate) {
    return (
      <EmptyState
        icon="📏"
        title="No Active Standard"
        description="Create a DBN scoring standard to define evaluation criteria."
        actionLabel="Create Standard"
        onAction={() => setShowCreate(true)}
      />
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">DBN Standards</h1>
        {!showCreate && (
          <Button onClick={() => setShowCreate(true)}>Create Standard</Button>
        )}
      </div>

      {showCreate && (
        <Card className="mb-6 p-6">
          <h2 className="mb-4 text-lg font-semibold text-gray-900">New Standard</h2>
          <div className="space-y-4">
            <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
            <Input label="Version" value={version} onChange={(e) => setVersion(e.target.value)} required />
            <div className="flex justify-end gap-3">
              <Button variant="secondary" onClick={() => setShowCreate(false)}>
                Cancel
              </Button>
              <Button onClick={handleCreate} loading={creating} disabled={!name || !version}>
                Create
              </Button>
            </div>
          </div>
        </Card>
      )}

      {standard && (
        <Card className="p-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-gray-900">{standard.name}</h2>
            <p className="text-sm text-gray-500">Version {standard.version}</p>
          </div>

          {standard.criteria.length === 0 ? (
            <p className="text-sm text-gray-500">No criteria defined yet.</p>
          ) : (
            <div className="space-y-3">
              {standard.criteria.map((c) => (
                <div key={c.id} className="rounded-lg border border-gray-200 p-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900">{c.name}</p>
                    <span className="text-xs text-gray-500">
                      Weight: {c.weight} / Max: {c.max_score}
                    </span>
                  </div>
                  {c.description && (
                    <p className="mt-1 text-xs text-gray-500">{c.description}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
