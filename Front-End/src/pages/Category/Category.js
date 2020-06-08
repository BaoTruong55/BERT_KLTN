import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
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
import './Category.scss';
import { DonutChart } from './components/DonutChart';
import { LineChart } from './components/LineChart';
import { Nodata } from '../Nodata/Nodata';

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
  const [category, setCategory] = React.useState(0);
  const [open, setOpen] = React.useState(false);
  const [convertRange, setConvertRange] = React.useState('');
  const [filter, setFilter] = React.useState(false);
  const [rangePicker, setRangePicker] = React.useState([
    {
      startDate: new Date(),
      endDate: null,
      key: 'selection',
    },
  ]);

  let moment = require('moment');

  const handleChange = (event) => {
    setCategory(event.target.value);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  /**
   * convert pick time => show time
   */
  function convertTime(time) {
    return moment
      .utc(time, 'ddd MMM DD YYYY HH:mm:ss ZZ')
      .add(1, 'days')
      .format('DD/MM/YYYY');
  }

  function handleSelect(item) {
    setRangePicker([item.selection]);
    let start = convertTime(item.selection.startDate);
    let end = convertTime(item.selection.endDate);
    setConvertRange(start + ' - ' + end);
  }

  const handleFilter = () => {
    setFilter(true);
  };

  return (
    <div>
      {/* ------------------------------------------------------------------------------------------------ */}
      <h1 className="h1 title">Category</h1>
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
                  <IconButton onClick={handleClickOpen}>
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
            onClose={handleClose}
            disableEscapeKeyDown
          >
            <DateRangePicker
              reditableDateInputs={true}
              showSelectionPreview={false}
              onChange={(item) => handleSelect(item)}
              moveRangeOnFirstSelection={false}
              ranges={rangePicker}
              maxDate={addDays(new Date(), 0)}
            />
            <DialogActions>
              <Button onClick={handleClose} color="primary">
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
      {/* ------------------------------------------------------------------------------------------------ */}
      {filter ? (
        <div className="row mt-5">
          <div className="col-md-6 col-sm 12">
            <div className="card">
              <h4 className="card-header">Pos and Neg</h4>
              <div className="card-body">
                <DonutChart data={[125, 50]} />
              </div>
            </div>
          </div>
          <div className="col-md-6 col-sm 12">
            <div className="card">
              <h4 className="card-header">Reaction of society</h4>
              <div className="card-body">
                <LineChart
                  dataPos={[65, 59, 80, 81, 56, 55, 40]}
                  dataNeg={[7, 2, 9, 2, 8.4, 7, 16]}
                />
              </div>
            </div>
          </div>
        </div>
      ) : (
        <Nodata />
      )}
    </div>
  );
};
