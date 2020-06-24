import React from 'react';
import { Line } from 'react-chartjs-2';

export const ConfirmedCaseChart = (props) => {
  const data = {
    labels: props.labels,
    datasets: [
      {
        label: 'Khỏi',
        lineTension: 0.1,
        backgroundColor: '#00945e',
        borderColor: '#00945e',
        borderCapStyle: 'butt',
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#00945e',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#00945e',
        pointHoverBorderColor: '#00945e',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: true,
        data: props.data2,
      },
      {
        label: 'Nhiễm',
        lineTension: 0.1,
        backgroundColor: '#9F224E',
        borderColor: '#9F224E',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: '#9F224E',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#9F224E',
        pointHoverBorderColor: '#9F224E',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: true,
        data: props.data1,
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
            maxTicksLimit: 10,
          },
        },
      ],
      yAxes: [
        {
          ticks: {
            maxTicksLimit: 10,
          },
        },
      ],
    },
  };

  return (
    <div>
      <Line data={data} options={options} />
    </div>
  );
};
