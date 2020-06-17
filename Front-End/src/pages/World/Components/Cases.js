import React from 'react';
import { Line } from 'react-chartjs-2';

export const CasesChart = (props) => {
  const data = {
    labels: props.labels,
    datasets: [
      {
        label: 'Đang điều trị',
        lineTension: 0.1,
        backgroundColor: 'rgba(255, 92, 0, 0.83)',
        borderColor: 'rgba(255, 92, 0, 1)',
        borderCapStyle: 'butt',
        borderDash: [],
        borderDashOffset: 0.0,
        borderJoinStyle: 'miter',
        pointBorderColor: 'rrgba(255, 92, 0, 1)',
        pointBackgroundColor: '#fff',
        pointBorderWidth: 1,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: 'rrgba(255, 92, 0, 1)',
        pointHoverBorderColor: 'rgba(220,220,220,1)',
        pointHoverBorderWidth: 2,
        pointRadius: 1,
        pointHitRadius: 10,
        fill: true,
        data: props.data,
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

  return (
    <div>
      <Line height={50} data={data} options={options} />
    </div>
  );
};
