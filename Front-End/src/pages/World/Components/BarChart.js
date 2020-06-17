import React from 'react';
import { Bar } from 'react-chartjs-2';

export const BarChart = (props) => {
  const data = {
    labels: props.labels,
    datasets: [
      {
        label: 'Khỏi',
        backgroundColor: '#00945e',
        borderColor: '#00945e',
        borderWidth: 1,
        hoverBackgroundColor: '#00945e',
        hoverBorderColor: '#00945e',
        data: props.data2,
      },
      {
        label: 'Nhiễm',
        backgroundColor: '#9F224E',
        borderColor: '#9F224E',
        borderWidth: 1,
        hoverBackgroundColor: '#9F224E',
        hoverBorderColor: '#9F224E',
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
      <Bar data={data} height={150} options={options} />
    </div>
  );
};
