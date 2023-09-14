import React from 'react';
import { Link } from 'react-router-dom';

const SideBarNavElement = ({ iconName, name, routeTo }) => {
  return (
    <li className="nav-item text-white fs-4 my-1 py-2 py-sm-0 ">
      <Link
        to={routeTo}
        className="nav-link text-white fs-5"
        aria-current="page"
      >
        <i className={`bi ${iconName}`}></i>
        <span className="ms-3 d-none d-sm-inline ">{name}</span>
      </Link>
    </li>
  );
};

export default SideBarNavElement;
