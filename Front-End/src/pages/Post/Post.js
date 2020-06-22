import React from 'react';
import './Post.scss';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { Button, AppBar, Tabs, Tab, Box } from '@material-ui/core';
import { DonutChart } from '../Category/components/DonutChart';
import { useTheme } from '@material-ui/core/styles';
import { Nodata } from '../Nodata/Nodata';
import axios from 'axios';
import { Loading } from '../../shared/Loading/Loading';
import { PostDetail } from '../../shared/PostDetail/PostDetail';

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
          <div>{children}</div>
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
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [data, setData] = React.useState();

  /**
   * Change value of tag
   * @param {*} event Event click
   * @param {*} newValue value of tab
   */
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  /**
   * Change index of tag
   * @param {*} index Index of tag
   */
  const handleChangeIndex = (index) => {
    setValue(index);
  };

  /**
   * get value of input 
   * @param {string} event Event on change
   */
  const getInput = (event) => {
    console.log(event.target.value);
    setLink(event.target.value);
  };

  /**
   * get data from link
   */
  const handleSearch = () => {
    if (link !== '') {
      setIsLoaded(true);
      axios
        .get(`${process.env.REACT_APP_LOCAL_URL}vnexpress?url=` + link)
        .then((res) => {
          setData(res.data);
          console.log(res.data);
          setSearch(true);
          setIsLoaded(false);
        })
        .catch((err) => {
          setIsLoaded(false);
          setSearch(false);
          alert('Oops, Something went wrong! Please try again.');
          console.log(err);
        });
    } else {
      setIsLoaded(false);
      setSearch(false);
    }
  };

  if (isLoaded) {
    return <Loading />;
  } else {
    return (
      <div>
        <h1 className="h1 title">Bài viết</h1>
        <div className="row">
          <div className="col-12 d-flex inputGroup">
            <input
              className="inputSearch input-group-text text-left"
              placeholder="Link của bài viết"
              onChange={getInput}
            />
            <Button
              onClick={handleSearch}
              variant="contained"
              className="btnSearch"
            >
              Tìm kiếm
            </Button>
          </div>
        </div>
        {search ? (
          <div className="row mt-5">
            <div className="col-md-6 col-sm-12">
              <PostDetail
                link={link}
                title={data.title}
                description={data.description}
                thumbnailUrl={data.thumbnailUrl}
              />
              <AppBar className="mt-5" position="static" color="default">
                <Tabs
                  value={value}
                  onChange={handleChange}
                  indicatorColor="primary"
                  textColor="primary"
                  variant="fullWidth"
                  aria-label="full width tabs example"
                >
                  <Tab label="Tích cực" {...a11yProps(0)} />
                  <Tab label="Tiêu cực" {...a11yProps(1)} />
                </Tabs>
              </AppBar>
              <SwipeableViews
                axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
                index={value}
                onChangeIndex={handleChangeIndex}
              >
                <TabPanel className="pd-0 tableComment" value={value} index={0}>
                  <table className="table table-striped">
                    <tbody>
                      {data.commentPos.map((e, index) => {
                        return (
                          <tr key={index}>
                            <th scope="row">{index + 1}</th>
                            <td><div dangerouslySetInnerHTML={{ __html: e.data_text }} /></td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </TabPanel>
                <TabPanel
                  className="pd-0 tableComment"
                  value={value}
                  index={1}
                  dir={theme.direction}
                >
                  <table className="table table-striped">
                    <tbody>
                      {data.commentNeg.map((e, index) => {
                        return (
                          <tr key={index}>
                            <th scope="row">{index + 1}</th>
                            <td>{e.data_text}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </TabPanel>
              </SwipeableViews>
            </div>
            <div className="col-md-6 col-sm-12 d-flex flex-column align-items-center">
              <h6>
                Biểu đồ thể hiện tỷ lệ Positive và Negative ở trong bài báo.
              </h6>
              <div className="chart">
                <DonutChart
                  data={[data.pos, data.neg]}
                  labels={['Tích cực', 'Tiêu cực']}
                />
              </div>
            </div>
          </div>
        ) : (
          <Nodata />
        )}
      </div>
    );
  }
}
