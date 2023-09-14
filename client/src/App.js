import React from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import { action as authAction } from './pages/Auth';

import AuthPage from './pages/Auth';
import HomePage from './pages/Home';
import SideBarLayout from './pages/SideBarLayout';
import DashboardPage from './pages/Dashboard';
import CustomersPage from './pages/Customers';
import ProductsPage from './pages/Products';
import OrdersPage from './pages/Orders';

const router = createBrowserRouter([
  {
    path: '/auth',
    element: <AuthPage />,
    action: authAction,
  },
  {
    path: '/',
    element: <SideBarLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'orders', element: <OrdersPage /> },
      { path: 'products', element: <ProductsPage /> },
      { path: 'customers', element: <CustomersPage /> },
    ],
  },
]);

function App() {
  const apiRoute = process.env.REACT_APP_API_URL || 'api/';
  localStorage.setItem('API_URL', apiRoute);

  return <RouterProvider router={router} />;
}

export default App;
