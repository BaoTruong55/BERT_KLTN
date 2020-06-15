import React from 'react';
import { Doughnut } from 'react-chartjs-2';

export const DonutChart = (props) => {
  const data = {
    labels: ['Pos', 'Neg'],
    datasets: [
      {
        data: props.data,
        backgroundColor: ['#FF6384', '#FFCE56'],
        hoverBackgroundColor: ['#ff1947', '#ffb711'],
        weight: 1,
      },
    ],
  };
  return (
    <div>
      <Doughnut data={data} />
    </div>
  );
};
