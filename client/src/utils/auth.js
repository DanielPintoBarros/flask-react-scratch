import { redirect } from 'react-router-dom';

export function getAuthToken() {
  const token = localStorage.getItem('accessToken');

  if (!token) {
    return null;
  }

  return token;
}

export function getRefreshToken() {
  const token = localStorage.getItem('refreshToken');

  if (!token) {
    return null;
  }

  return token;
}

export function tokenLoader() {
  const token = getAuthToken();
  return token;
}

export function checkAuthLoader() {
  const token = getAuthToken();

  if (!token) {
    return redirect('/auth');
  }
}

export function setAccessToken(accessToken) {
  if (accessToken) {
    localStorage.setItem('accessToken', accessToken);
  } else {
    localStorage.removeItem('accessToken');
  }
}

export function setTokenCredentials(accessToken, refreshToken) {
  if (accessToken) {
    localStorage.setItem('accessToken', accessToken);
  } else {
    localStorage.removeItem('accessToken');
  }

  if (refreshToken) {
    localStorage.setItem('refreshToken', refreshToken);
  } else {
    localStorage.removeItem('refreshToken');
  }
}

export async function refreshToken() {
  const accessToken = getAuthToken();
  const refreshToken = getRefreshToken();
  if (accessToken && refreshToken) {
    const response = await fetch(
      `${localStorage.getItem('API_URL')}/refreshToken`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${refreshToken}`,
        },
      }
    );
    if (response.ok) {
      const data = await response.json();
      setAccessToken(data['access_token']);
      return;
    }
  }
  setTokenCredentials(null, null);
}

export async function logout() {
  const accessToken = getAuthToken();

  if (accessToken) {
    fetch(`${localStorage.getItem('API_URL')}/logout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    });
  }
  setTokenCredentials(null, null);
}
