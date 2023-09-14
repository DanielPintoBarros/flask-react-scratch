import React from 'react';
import './SideBar.css';
import SideBarNavElement from './SideBarNavElement';
import AccountSide from './AccountSide';
import { Link } from 'react-router-dom';
const SideBar = () => {
  const navOptions = [
    { name: 'Dashboard', iconName: 'bi-speedometer2', routeTo: '/dashboard' },
    { name: 'Home', iconName: 'bi-house', routeTo: '/' },
    { name: 'Orders', iconName: 'bi-table', routeTo: '/orders' },
    { name: 'Products', iconName: 'bi-grid', routeTo: '/products' },
    { name: 'Customers', iconName: 'bi-people', routeTo: '/customers' },
  ];

  return (
    <div className="bg-dark col-auto col-md-2 min-vh-100 d-flex justify-content-between flex-column">
      <div>
        <Link
          to={'/'}
          className="text-decoration-none text-white d-none d-sm-inline d-flex align-itemcenter ms-3 mt-2"
        >
          <span className="ms-1 py-2 py-sm-0 fs-4 d-non d-sm-inline">
            Brand
          </span>
        </Link>
        <hr className="text-secondary d-none d-sm-block" />
        <ul className="nav nav-pills flex-column mt-3 mt-sm-0">
          {navOptions.map((nav) => {
            return (
              <SideBarNavElement
                key={nav.name}
                name={nav.name}
                iconName={nav.iconName}
                routeTo={nav.routeTo}
              />
            );
          })}
        </ul>
      </div>
      <AccountSide />
    </div>
  );
};

export default SideBar;
