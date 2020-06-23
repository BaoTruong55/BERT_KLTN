import React, { useEffect } from 'react';
import { AppBar, Tabs, Tab } from '@material-ui/core';
import Homepage from '../Homepage/Homepage';
import { Category } from '../Category/Category';
import { World } from '../World/World';
import { Post } from '../Post/Post';
import { Topic } from '../Topic/Topic';
import './Header.scss';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import { useLocation } from 'react-router';
import Logo from '../../assets/img/logo.png';
import {
  Navbar,
  NavbarBrand,
  NavbarNav,
  NavItem,
  NavLink,
  NavbarToggler,
  Collapse,
  FormInline,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Fa,
} from 'mdbreact';

export default function NavTabs() {
  const [value, setValue] = React.useState(0);
  const [isOpen, setIsOpen] = React.useState(false);

  const toggleCollapse = () => {
    setIsOpen(!isOpen);
  };

  return (
    <Router>
      <Navbar
        color="primary-color"
        light
        expand="md"
        scrolling={true}
      >
        <NavbarBrand>
          <img src={Logo} alt=""/>
        </NavbarBrand>
        <NavbarToggler onClick={toggleCollapse} />
        <Collapse id="navbarCollapse3" isOpen={isOpen} navbar>
          <NavbarNav left>
            <NavItem>
              <NavLink exact to="/">Trang chủ</NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="/vietnam">Việt Nam</NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="/ros">Covid</NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="/post">Bài viết</NavLink>
            </NavItem>
            <NavItem>
              <NavLink to="/topic">Chủ đề nổi bật</NavLink>
            </NavItem>
          </NavbarNav>

          <NavbarNav right>
            <NavItem>
              <NavLink className="waves-effect waves-light" to="#!">
                <Fa icon="twitter" />
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink className="waves-effect waves-light" to="#!">
                <Fa icon="google-plus" />
              </NavLink>
            </NavItem>
          </NavbarNav>
        </Collapse>
      </Navbar>
      <div className="component">
          <Route exact path="/" component={Homepage} />
          <Route path="/vietnam" component={World} />
          <Route path="/ros" component={Category} />
          <Route path="/post" component={Post} />
          <Route path="/topic" component={Topic} />
        </div>
    </Router>
  );
}
