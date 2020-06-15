import React from 'react'
import {Polar} from 'react-chartjs-2';

export const PolarChart = (props) => {
    const data = {
        datasets: [{
          data: props.data,
          backgroundColor: [
            '#FF6384',
            '#FFCE56',
          ],
        }],
        labels: props.labels
      };
    return (
        <div>
            <Polar data={data} />
        </div>
    )
}
