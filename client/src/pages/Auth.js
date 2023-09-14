import React, { useEffect } from 'react';

import AuthForm from '../components/Auth/AuthForm';
import { getAuthToken, setTokenCredentials } from '../utils/auth';
import { json, redirect, useNavigate } from 'react-router-dom';

const AuthPage = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const isLogged = !!getAuthToken();
    if (isLogged) navigate('/');
  }, []);
  return <AuthForm />;
};

export default AuthPage;

export async function action({ request }) {
  const searchParams = new URL(request.url).searchParams;
  const redirectTo = searchParams.get('redirectTo') || '/';

  const data = await request.formData();
  const authData = {
    email: data.get('email'),
    password: data.get('password'),
  };

  const response = await fetch(`${localStorage.getItem('API_URL')}/auth`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(authData),
  });
  if (response.ok) {
    const resData = await response.json();
    setTokenCredentials(resData['access_token'], resData['refresh_token']);

    return redirect(redirectTo);
  } else if (response.status === 401) {
    return response;
  }

  throw json({ message: 'Could not authenticate user.' }, { status: 500 });
}
