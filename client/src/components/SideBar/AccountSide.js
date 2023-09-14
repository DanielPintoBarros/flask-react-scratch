import React from 'react';
import { Link } from 'react-router-dom';

const AccountSide = () => {
  return (
    <div className="dropdown open ">
      <a
        className="text-decoration-none text-white dropdown-toggle p-3 "
        type="button"
        id="triggerId"
        data-bs-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
      >
        <i className="bi bi-person-circle"></i>
        <span className="fs-5 ms-2 d-none d-sm-inline">Account</span>
      </a>

      <div className="dropdown-menu" aria-labelledby="triggerId">
        <Link className="dropdown-item disabled" to="#">
          <span className="fs-6">Change Password</span>
        </Link>
        <Link className="dropdown-item disabled" to="#">
          <span className="fs-6">Settings</span>
        </Link>
        <Link className="dropdown-item disabled" to="#">
          <span className="fs-6">Logout</span>
        </Link>
      </div>
    </div>
  );
};

export default AccountSide;
