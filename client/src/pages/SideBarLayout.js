import React, { useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { getAuthToken } from '../utils/auth';
import SideBar from '../components/SideBar/SideBar';

const SideBarLayout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const isLogged = !!getAuthToken();
    if (!isLogged) navigate('/auth');
  });

  return (
    <main className="d-flex flex-nowrap row vh-100">
      <SideBar />
      <Outlet />
    </main>
  );
};

export default SideBarLayout;
