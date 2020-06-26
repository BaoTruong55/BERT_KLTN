import React from 'react';
import Homepage from '../Homepage/Homepage';
import { Category } from '../Category/Category';
import { World } from '../World/World';
import { Post } from '../Post/Post';
import { Topic } from '../Topic/Topic';
import './Header.scss';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Logo from '../../assets/img/logo.png';
import {
  Navbar,
  NavbarBrand,
  NavbarNav,
  NavItem,
  NavLink,
  NavbarToggler,
  Collapse,
} from 'mdbreact';

export default function NavTabs() {
  const [isOpen, setIsOpen] = React.useState(false);

  const toggleCollapse = () => {
    setIsOpen(!isOpen);
  };

  const handleOpen = () => {
    setIsOpen(false);
  };

  return (
    <Router>
      <Navbar
        color="primary-color"
        light
        expand="md"
        scrolling={true}
        className="border-bottom shadow-sm pt-0 pb-0"
      >
        <NavbarBrand>
          <img src={Logo} alt="" className="logo"/>
        </NavbarBrand>
        <NavbarToggler onClick={toggleCollapse} />
        <Collapse id="navbarCollapse3" isOpen={isOpen} navbar>
          <NavbarNav right>
            <NavItem className="pr-2">
              <NavLink onClick={handleOpen} exact to="/">
                Trang chủ
              </NavLink>
            </NavItem>
            <NavItem className="pr-2">
              <NavLink onClick={handleOpen} to="/vietnam">
                Việt Nam
              </NavLink>
            </NavItem>
            <NavItem className="pr-2">
              <NavLink onClick={handleOpen} to="/ros">
                Covid
              </NavLink>
            </NavItem>
            <NavItem className="pr-2">
              <NavLink onClick={handleOpen} to="/post">
                Bài viết
              </NavLink>
            </NavItem>
            <NavItem className="pr-2">
              <NavLink onClick={handleOpen} to="/topic">
                Chủ đề nổi bật
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
