type QueryValue = string | number | boolean | null | undefined;

export type ApiResult<T> = {
  data: T | null;
  error: string | null;
  status: number | null;
};

const defaultBaseUrl = 'http://localhost:8000';

function getApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_API_URL ?? defaultBaseUrl;
}

function buildApiUrl(path: string, params?: Record<string, QueryValue>): string {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  const url = new URL(normalizedPath, getApiBaseUrl());
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value === null || value === undefined || value === '') {
        continue;
      }
      url.searchParams.set(key, String(value));
    }
  }
  return url.toString();
}

export async function apiGet<T>(
  path: string,
  params?: Record<string, QueryValue>
): Promise<ApiResult<T>> {
  const url = buildApiUrl(path, params);
  try {
    const response = await fetch(url, { cache: 'no-store' });
    if (!response.ok) {
      let detail = '';
      try {
        const payload = (await response.json()) as { detail?: string };
        if (payload?.detail) {
          detail = `: ${payload.detail}`;
        }
      } catch {
        detail = '';
      }
      return {
        data: null,
        error: `Erro ${response.status}${detail}`,
        status: response.status,
      };
    }
    const data = (await response.json()) as T;
    return { data, error: null, status: response.status };
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Falha de rede';
    return { data: null, error: message, status: null };
  }
}
