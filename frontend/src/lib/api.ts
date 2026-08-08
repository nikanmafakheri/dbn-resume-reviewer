/**
 * Central API configuration + a tiny typed fetch wrapper.
 *
 * The backend runs on `localhost:8000` during development. Point this at
 * your deployed API before shipping — either by editing the default or by
 * overriding via the `VITE_API_BASE_URL` environment variable.
 */
export const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? '/api/v1';

export interface ApiError {
  status: number;
  detail: string;
}

const DEFAULT_TIMEOUT_MS = 20_000;

/**
 * True when a failure is a transient capacity pause rather than a bug.
 * Matches HTTP 429, the API's `Too many requests`, the backend's structured
 * `error_code` for quota (`rate_limited`) and timeout (`timed_out`), plus
 * provider strings that carry "quota"/"rate limit"/"exceeded"/timeout terms.
 *
 * A timed-out provider request is surfaced the same way as a quota pause:
 * the friendly amber "please wait & retry" card with auto-retry.
 */
export function isRateLimitError(
  status?: number | null,
  message?: string | null,
): boolean {
  if (status === 429) return true;
  const text = message ?? '';
  return /rate.limit|quota|exceeded|too many requests|429|timed out|timeout|deadline|cancelled/i.test(text);
}

/**
 * Typed GET helper with timeout + sane error mapping.
 * Use for all read paths so failures surface consistently.
 */
export async function apiGet<T>(path: string, signal?: AbortSignal): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);
  const onExternalAbort = () => controller.abort();
  signal?.addEventListener('abort', onExternalAbort, { once: true });

  try {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      signal: controller.signal,
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) {
      let detail = `Request failed (${res.status})`;
      try {
        const body = await res.json();
        if (body?.detail) detail = typeof body.detail === 'string' ? body.detail : detail;
      } catch {
        /* non-JSON error body — keep default */
      }
      const err = new Error(detail) as Error & ApiError;
      err.status = res.status;
      throw err;
    }
    return (await res.json()) as T;
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener('abort', onExternalAbort);
  }
}

/**
 * POST a JSON body. Returns parsed JSON on success.
 */
export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: 'POST',
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const json = await res.json();
      if (json?.detail) detail = typeof json.detail === 'string' ? json.detail : detail;
    } catch {
      /* ignore */
    }
    const err = new Error(detail) as Error & ApiError;
    err.status = res.status;
    throw err;
  }
  return (await res.json()) as T;
}
