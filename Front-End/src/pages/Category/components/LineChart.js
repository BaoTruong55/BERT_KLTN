import React from 'react';
import { Line } from 'react-chartjs-2';

export const LineChart = (props) => {
  const data = {
    labels: props.labels,
    datasets: [
      {
        label: 'Tích cực',
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#FF6384',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#FF6384',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 3,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#FF6384',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: false,
        data: props.dataPos,
      },
      {
        label: 'Tiêu cực',
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#FFCE56',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#FFCE56',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 3,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#FFCE56',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: false,
        data: props.dataNeg,
      },
      {
        label: 'Số bài viết',
        lineTension: 0.1,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: '#00945e',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#00945e',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 3,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#00945e',
        pointHoverBorderColor: '#00945e',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: false,
        data: props.dataPost,
      },
    ],
  };

  const options = {
    tooltips: {
      mode: 'x-axis',
      intersect: false,
    },
    scales: {
      xAxes: [
        {
          ticks: {
            maxTicksLimit: 5,
          },
          gridLines: {
            display: false,
          },
        },
      ],
      yAxes: [
        {
          ticks: {
            maxTicksLimit: 5,
          },
          gridLines: {
            display: true,
          },
        },
      ],
    },
  };

  const handleClick = (elems, event) => {
    // console.log(elems);
    if (elems.length !== 0) {
      props.onReturnData(data.labels[elems[0]._index]);
    }
  };

  return (
    <div>
      <Line data={data} options={options} getElementsAtEvent={handleClick} />
    </div>
  );
};
