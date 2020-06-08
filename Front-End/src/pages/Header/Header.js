import React from 'react';
import { AppBar, Tabs, Tab } from '@material-ui/core';
import Homepage from '../Homepage/Homepage';
import { Category } from '../Category/Category';
import { World } from '../World/World';
import { Post } from '../Post/Post';
import './Header.scss';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

export default function NavTabs() {
  const [value, setValue] = React.useState(0);

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
            <Tab label="World" component={Link} to="/world" />
            <Tab label="Category" component={Link} to="/category" />
            <Tab label="Post" component={Link} to="/post" />
          </Tabs>
        </AppBar>
        <div className="component">
          <Route exact path="/" component={Homepage} />
          <Route path="/world" component={World} />
          <Route path="/category" component={Category} />
          <Route path="/post" component={Post} />
        </div>
      </div>
    </Router>
  );
}
