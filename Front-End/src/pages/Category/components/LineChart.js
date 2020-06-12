import React from 'react';
import { Line } from 'react-chartjs-2';

export const LineChart = (props) => {
  const data = {
    labels: props.labels,
    datasets: [
      {
        label: 'Pos',
        lineTension: 0.5,
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
        label: 'Neg',
        lineTension: 0.5,
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
    ],
  };

  return (
    <div>
      <Line data={data} />
    </div>
  );
};
