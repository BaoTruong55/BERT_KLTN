import React, { useEffect, useState } from 'react';
import './Topic.scss';
import { makeStyles } from '@material-ui/core/styles';
import WordCloud from './components/WordCloud';
import {
  InputLabel,
  MenuItem,
  FormControl,
  Select,
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
import './Topic.scss';
import { Nodata } from '../Nodata/Nodata';
import axios from 'axios';
import { Loading } from '../../shared/Loading/Loading';
// import axios from 'axios';

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

export const Topic = () => {
  // const [topics, setTopics] = useState();
  const [category, setCategory] = React.useState(0);
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);
  const [convertRange, setConvertRange] = React.useState('');
  const [filter, setFilter] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
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

  const handleChange = (event) => {
    setCategory(event.target.value);
  };

  const handleDialog = () => {
    setOpen(!open);
  };

  /**
   * convert pick time => show time
   */
  function convertTime(time) {
    return moment
      .utc(time, 'ddd MMM DD YYYY HH:mm:ss ZZ')
      .add(1, 'days')
      .format('MM/DD/YYYY');
  }

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

  const handleFilter = () => {
    console.log(rangeFormat);
    setLoading(true);
    setFilter(true);
    axios
      .get(
        'http://127.0.0.1:5000/vnexpress/covid?datefrom=' +
          rangeFormat.startDate +
          '&dateto=' +
          rangeFormat.endDate
      )
      .then((res) => {
        console.log(res.data);
        let labels = [];
        let dataPos = [];
        let dataNeg = [];
        if (res && res.data && res.data.sentiment_by_date) {
          // setData here
          setFilter(true);
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

  const topic = {
    topics: [
      {
        id: '1751295897__Berlin',
        label: 'Berlin',
        volume: 165,
        type: 'topic',
        sentiment: {
          negative: 3,
          neutral: 133,
          positive: 29,
        },
        sentimentScore: 65,
      },
      {
        id: '1751295897__DJ',
        label: 'DJ',
        volume: 48,
        type: 'topic',
        sentiment: {
          neutral: 46,
          positive: 2,
        },
        sentimentScore: 54,
      },
      {
        id: '1751295897__Ostgut Ton',
        label: 'Ostgut Ton',
        volume: 24,
        type: 'topic',
        sentiment: {
          neutral: 22,
          positive: 2,
        },
        sentimentScore: 58,
      },
      {
        id: '1751295897__Hammered',
        label: 'Hammered',
        volume: 48,
        type: 'topic',
        sentiment: {
          neutral: 18,
          negative: 30,
        },
        sentimentScore: 20,
      },
      {
        id: '1751295897__Code',
        label: 'Code',
        volume: 16,
        type: 'topic',
        sentiment: {
          neutral: 13,
          positive: 3,
        },
        sentimentScore: 68,
      },
      {
        id: '1751295897__Quantified Drunk',
        label: 'Quantified Drunk',
        volume: 14,
        type: 'topic',
        sentiment: {
          neutral: 14,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Berghain resident',
        label: 'Berghain resident',
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 10,
          positive: 3,
        },
        sentimentScore: 73,
      },
      {
        id: "1751295897__San Soda's Panorama Bar",
        label: "San Soda's Panorama Bar",
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 13,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Germany',
        label: 'Germany',
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 9,
          positive: 4,
        },
        sentimentScore: 80,
      },
      {
        id: '1751295897__Amsterdam',
        label: 'Amsterdam',
        volume: 12,
        type: 'topic',
        sentiment: {
          neutral: 7,
          positive: 5,
        },
        sentimentScore: 91,
      },
      {
        id: '1751295897__Kantine am Berghain',
        label: 'Kantine am Berghain',
        volume: 11,
        type: 'topic',
        sentiment: {
          neutral: 10,
          positive: 1,
        },
        sentimentScore: 59,
      },
      {
        id: '1751295897__London',
        label: 'London',
        volume: 11,
        type: 'topic',
        sentiment: {
          neutral: 8,
          positive: 3,
        },
        sentimentScore: 77,
      },
      {
        id: '1751295897__UK',
        label: 'UK',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 8,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Marcel Dettmann',
        label: 'Marcel Dettmann',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 5,
          positive: 3,
        },
        sentimentScore: 87,
      },
      {
        id: '1751295897__Disco',
        label: 'Disco',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 8,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Barcelona',
        label: 'Barcelona',
        volume: 7,
        type: 'topic',
        sentiment: {
          neutral: 7,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Watergate',
        label: 'Watergate',
        volume: 7,
        type: 'topic',
        sentiment: {
          neutral: 6,
          positive: 1,
        },
        sentimentScore: 64,
      },
      {
        id: '1751295897__debut LP',
        label: 'debut LP',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 3,
        },
        sentimentScore: 100,
      },
      {
        id: '1751295897__Patrick Gräser',
        label: 'Patrick Gräser',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 3,
        },
        sentimentScore: 100,
      },
      {
        id: '1751295897__Panorama Bar in Berlin',
        label: 'Panorama Bar in Berlin',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 4,
          positive: 2,
        },
        sentimentScore: 83,
      },
      {
        id: '1751295897__legendary nightclub',
        label: 'legendary nightclub',
        volume: 6,
        type: 'topic',
        sentiment: {
          positive: 6,
        },
        sentimentScore: 150,
      },
      {
        id: '1751295897__Ben Klock',
        label: 'Ben Klock',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Mixes',
        label: 'Mixes',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Panorama Bar Music',
        label: 'Panorama Bar Music',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Terrace Sundae',
        label: 'Terrace Sundae',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Jun',
        label: 'Jun',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__Live set',
        label: 'Live set',
        volume: 4,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 1,
        },
        sentimentScore: 75,
      },
      {
        id: '1751295897__dance music',
        label: 'dance music',
        volume: 4,
        type: 'topic',
        sentiment: {
          neutral: 4,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__club culture',
        label: 'club culture',
        volume: 3,
        type: 'topic',
        sentiment: {
          neutral: 3,
        },
        sentimentScore: 50,
      },
      {
        id: '1751295897__D/B Presents',
        label: 'D/B Presents',
        volume: 3,
        type: 'topic',
        sentiment: {
          neutral: 3,
        },
        sentimentScore: 50,
      },
    ],
  };

  return (
    <div>
      <h1 className="h1 title">Topic</h1>
      <div className="row">
        <div className="col-12 d-flex align-items-center">
          <FormControl className={classes.formControl}>
            <InputLabel>Categories</InputLabel>
            <Select value={category} onChange={handleChange}>
              <MenuItem value={0}>Thế giới</MenuItem>
              <MenuItem value={1}>Sức khỏe</MenuItem>
              <MenuItem value={2}>Kinh doanh</MenuItem>
              <MenuItem value={3}>Thể thao</MenuItem>
              <MenuItem value={4}>Du lịch</MenuItem>
              <MenuItem value={5}>Giải trí</MenuItem>
              <MenuItem value={6}>Cộng đồng</MenuItem>
            </Select>
          </FormControl>

          <FormControl className={classes.formControl}>
            <InputLabel className="" htmlFor="standard-adornment-password">
              Time
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
                Agree
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
            Filter
          </Button>
        </div>
      </div>
      {/* ----------------------------- Filter -----------------------------*/}
      {filter ? (
        <div className="row">
          <WordCloud topics={topic.topics} />
        </div>
      ) : (
        <Nodata />
      )}
    </div>
  );
};
