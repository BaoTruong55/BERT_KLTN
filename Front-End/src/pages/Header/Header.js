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

export default function NavTabs() {
  const [value, setValue] = React.useState(0);
  let location = useLocation();
  useEffect(() => {
    const getParam = () => {
      switch (location.pathname) {
        case '/':
          setValue(0);
          break;
        case '/vietnam':
          setValue(1);
          break;
        case '/ros':
          setValue(2);
          break;
        case '/post':
          setValue(3);
          break;
        case '/topic':
          setValue(4);
          break;
        default:
          break;
      }
    };
    getParam();
  }, [location.pathname]);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Router>
      <div>
        <AppBar position="static" color="default">
          <Tabs
            value={value}
            onChange={handleChange}
            aria-label="nav tabs example"
          >
            <Tab label="Home" component={Link} to="/" />
            <Tab label="Việt Nam" component={Link} to="/vietnam" />
            <Tab label="RoS" component={Link} to="/ros" />
            <Tab label="Post" component={Link} to="/post" />
            <Tab label="Topic" component={Link} to="/topic" />
          </Tabs>
        </AppBar>
        <div className="component">
          <Route exact path="/" component={Homepage} />
          <Route path="/vietnam" component={World} />
          <Route path="/ros" component={Category} />
          <Route path="/post" component={Post} />
          <Route path="/topic" component={Topic} />
        </div>
      </div>
    </Router>
  );
}
