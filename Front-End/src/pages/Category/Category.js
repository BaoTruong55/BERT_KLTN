import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
  InputLabel,
  FormControl,
  Button,
  Dialog,
  DialogActions,
  Slide,
  InputAdornment,
  IconButton,
  Input,
} from '@material-ui/core/';
import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css';
import { DateRangePicker } from 'react-date-range';
import { addDays } from 'date-fns';
import DateRangeIcon from '@material-ui/icons/DateRange';
import './Category.scss';
import { DonutChart } from './components/DonutChart';
import { LineChart } from './components/LineChart';
import { Nodata } from '../Nodata/Nodata';
import axios from 'axios';
import { Loading } from '../../shared/Loading/Loading';
import { PostDetail } from '../../shared/PostDetail/PostDetail';
const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

export const Category = () => {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  const [convertRange, setConvertRange] = React.useState('');
  const [filter, setFilter] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [displayTop, setDisplayTop] = React.useState(false);
  const [displayPost, setDisplayPost] = React.useState(false);
  const [dataPost, setDataPost] = React.useState();
  const [data, setData] = React.useState({
    data: {
      allData: [],
      labels: [],
      dataPos: [],
      dataNeg: [],
      totalPos: 0,
      totalNeg: 0,
      top_pos: [],
      countPost: [],
    },
  });
  const [rangePicker, setRangePicker] = React.useState([
    {
      startDate: new Date(),
      endDate: null,
      key: 'selection',
    },
  ]);
  const [rangeFormat, setRangeFormat] = React.useState({
    startDate: '',
    endDate: '',
  });

  let moment = require('moment');

  const handleDialog = () => {
    setOpen(!open);
  };

  /**
   * Convert time before Show time on DateRangePicker and return Date MM/DD/YYYY
   * @param {Date} time ddd MMM DD YYYY HH:mm:ss ZZ
   */
  function convertTime(time) {
    return moment
      .utc(time, 'ddd MMM DD YYYY HH:mm:ss ZZ')
      .add(1, 'days')
      .format('MM/DD/YYYY');
  }

  /**
   *  Handle date and time, then setRangeFormat and setConvertRange
   * @param {Date} item DateRangePicker
   */
  function handleSelect(item) {
    setRangePicker([item.selection]);
    let start = convertTime(item.selection.startDate);
    let end = convertTime(item.selection.endDate);
    setRangeFormat({
      startDate: start,
      endDate: end,
    });
    setConvertRange(start + ' - ' + end);
  }

  const getReturnData = (e) => {
    // console.log(e);
    let resData = data.data.allData.filter((elems) => elems.date === e);
    setDataPost(resData[0]);
    setDisplayTop(false);
    setDisplayPost(true);
  };

  /**
   * fetch data from post's link
   */
  const handleFilter = () => {
    // console.log(rangeFormat);
    setLoading(true);
    setFilter(true);
    axios
      .get(
        `${process.env.REACT_APP_API_BASE_URL}vnexpress/covid?datefrom=` +
          rangeFormat.startDate +
          '&dateto=' +
          rangeFormat.endDate
      )
      .then((res) => {
        // console.log(res.data);
        let labels = [];
        let dataPos = [];
        let dataNeg = [];
        let top_post = [];
        if (res && res.data) {
          if (res.data.sentiment_by_date) {
            for (let i = 0; i < res.data.sentiment_by_date.length; i++) {
              labels.push(res.data.sentiment_by_date[i].date);
              dataPos.push(res.data.sentiment_by_date[i].data.pos);
              dataNeg.push(res.data.sentiment_by_date[i].data.neg);
            }
          }

          if (res.data.top_post) {
            for (let i = 0; i < res.data.top_post.length; i++) {
              top_post.push(res.data.top_post[i]);
            }
          }

          setData({
            ...data,
            data: {
              allData: res.data.sentiment_by_date,
              labels: labels,
              dataPos: dataPos,
              dataNeg: dataNeg,
              totalPos: res.data.total_pos,
              totalNeg: res.data.total_neg,
              top_post: top_post,
              countPost: res.data.sentiment_by_date.map((e) => {
                return e.data.count_post;
              }),
            },
          });
          setFilter(true);
          setDisplayTop(true);
          setDisplayPost(false);
          setLoading(false);
        } else {
          setFilter(false);
          setLoading(false);
          alert('Oops, Something went wrong! Please try again.');
        }
      })
      .catch((err) => {
        setFilter(false);
        setLoading(false);
        alert('Oops, Something went wrong! Please try again.');
        console.log(err);
      });
  };

  if (loading) {
    return <Loading />;
  } else {
    return (
      <div>
        {/* ------------------------------------------------------------------------------------------------ */}
        <h1 className="h1 title">Phản ứng của xã hội</h1>
        <div className="row">
          <div className="col-12 d-flex align-items-center">
            <FormControl className={classes.formControl}>
              <InputLabel className="" htmlFor="standard-adornment-password">
                Thời gian
              </InputLabel>
              <Input
                className=""
                required
                id="standard-required"
                label="Required"
                disabled
                value={convertRange}
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton onClick={handleDialog}>
                      <DateRangeIcon />
                    </IconButton>
                  </InputAdornment>
                }
              />
            </FormControl>

            <Dialog
              open={open}
              TransitionComponent={Transition}
              keepMounted
              onClose={handleDialog}
              disableEscapeKeyDown
              disableBackdropClick={true}
            >
              <DateRangePicker
                reditableDateInputs={true}
                showSelectionPreview={false}
                onChange={(item) => handleSelect(item)}
                moveRangeOnFirstSelection={false}
                ranges={rangePicker}
                maxDate={addDays(new Date(), 0)}
                minDate={addDays(new Date(), -30)}
                dragSelectionEnabled={false}
              />
              <DialogActions>
                <Button onClick={handleDialog} color="primary">
                  Đồng ý
                </Button>
              </DialogActions>
            </Dialog>
            <Button
              disabled={convertRange === '' ? true : false}
              variant="contained"
              color="primary"
              className="filterBtn"
              onClick={handleFilter}
            >
              Lọc
            </Button>
          </div>
        </div>
        {/* ------------------------------------------------------------------------------------------------ */}
        {filter ? (
          <div className="mt-5">
            <div className="row">
              <div className="col-md-6 col-sm 12 mr-b">
                <div className="card">
                  <h4 className="card-header">Tích cực và Tiêu cực</h4>
                  <div className="card-body">
                    <DonutChart
                      data={[data.data.totalPos, data.data.totalNeg]}
                      labels={['Tích cực', 'Tiêu cực']}
                    />
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-sm 12 mr-b">
                <div className="card">
                  <h4 className="card-header">Phản ứng của xã hội</h4>
                  <div className="card-body">
                    <LineChart
                      onReturnData={getReturnData}
                      dataPos={data.data.dataPos}
                      dataNeg={data.data.dataNeg}
                      dataPost={data.data.countPost}
                      labels={data.data.labels}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-5">
              {(data.data.top_post == null && displayTop) ||
              (dataPost == null && displayPost) ? (
                <div>Không có bài viết</div>
              ) : displayTop ? (
                <h2>Bài viết tiêu biểu:</h2>
              ) : displayPost ? (
                <h2>Bài viết trong ngày {dataPost.date}:</h2>
              ) : (
                <div></div>
              )}
            </div>
            <div className="d-flex flex-column align-items-center">
              <div className="top-post">
                {(data.data.top_post == null && displayTop) ||
                (dataPost == null && displayPost) ? (
                  <div></div>
                ) : displayTop ? (
                  data.data.top_post.map((e, index) => {
                    return (
                      <PostDetail
                        key={index}
                        link={e.url}
                        title={e.title}
                        description={e.description}
                        thumbnailUrl={e.thumbnailUrl}
                      />
                    );
                  })
                ) : displayPost ? (
                  dataPost.data.posts.map((e, index) => {
                    return (
                      <PostDetail
                        key={index}
                        link={e.url}
                        title={e.title}
                        description={e.description}
                        thumbnailUrl={e.thumbnailUrl}
                      />
                    );
                  })
                ) : (
                  <div></div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <Nodata />
        )}
      </div>
    );
  }
};
