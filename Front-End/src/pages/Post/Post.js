import React from 'react';
import './Post.scss';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { Button, AppBar, Tabs, Tab, Typography, Box } from '@material-ui/core';
import { DonutChart } from '../Category/components/DonutChart';
import { useTheme } from '@material-ui/core/styles';
import { Nodata } from '../Nodata/Nodata';
import axios from 'axios';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`full-width-tabpanel-${index}`}
      aria-labelledby={`full-width-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box p={3}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `full-width-tab-${index}`,
    'aria-controls': `full-width-tabpanel-${index}`,
  };
}

export function Post() {
  const theme = useTheme();
  const [value, setValue] = React.useState(0);
  const [search, setSearch] = React.useState(false);
  const [link, setLink] = React.useState('');

  const [error, setError] = React.useState(null);
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [items, setItems] = React.useState([]);
  const [data, setData] = React.useState();

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const handleChangeIndex = (index) => {
    setValue(index);
  };

  const getInput = (event) => {
    console.log(event.target.value);
    setLink(event.target.value);
  };

  const handleSearch = () => {
    axios
      .get(`http://127.0.0.1:5000/vnexpress?url=` + link)
      .then((res) => {
        setData(res.data);
        console.log(res.data);
        setSearch(true);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div>
      <h1 className="h1 title">Post</h1>
      <div className="row">
        <div className="col-4 d-flex inputGroup">
          <input
            className="inputSearch input-group-text text-left"
            placeholder="Post's link"
            onChange={getInput}
          />
          <Button
            onClick={handleSearch}
            variant="contained"
            className="btnSearch"
          >
            Search
          </Button>
        </div>
      </div>
      {search ? (
        <div className="row mt-5">
          <div className="col-md-4 col-sm-12">
            <h2>{data.title}</h2>
            <p>{data.description}</p>
            <AppBar className="mt-5" position="static" color="default">
              <Tabs
                value={value}
                onChange={handleChange}
                indicatorColor="primary"
                textColor="primary"
                variant="fullWidth"
                aria-label="full width tabs example"
              >
                <Tab label="Positive" {...a11yProps(0)} />
                <Tab label="Negative" {...a11yProps(1)} />
              </Tabs>
            </AppBar>
            <SwipeableViews
              axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
              index={value}
              onChangeIndex={handleChangeIndex}
            >
              <TabPanel className="pd-0" value={value} index={0}>
                <table className="table table-striped">
                  <tbody>
                    {data.commentPos.map((e, index) => {
                      return (
                        <tr>
                          <th scope="row">{index}</th>
                          <td>{e.name}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </TabPanel>
              <TabPanel value={value} index={1} dir={theme.direction}>
                <table className="table table-striped">
                  <tbody>
                    {data.commentNeg.map((e, index) => {
                      return (
                        <tr>
                          <th scope="row">{e.id}</th>
                          <td>{e.name}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </TabPanel>
            </SwipeableViews>
          </div>
          <div className="col-md-8 col-sm-12 d-flex flex-column align-items-center">
            <h6>
              Biểu đồ thể hiện tỷ lệ Positive và Negative ở trong bài báo.
            </h6>
            <div className="chart">
              <DonutChart data={[54, 31]} />
            </div>
          </div>
        </div>
      ) : (
        <Nodata />
      )}
    </div>
  );
}