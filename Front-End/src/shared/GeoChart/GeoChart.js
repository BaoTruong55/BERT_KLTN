import React from 'react';
import { Chart } from 'react-google-charts';

export const GeoChart = () => {
  return (
    <div>
      <Chart
        width={'500px'}
        height={'300px'}
        chartType="GeoChart"
        data={[
          ['City', 'Population', 'Area'],
          ['Ha Noi', 2761477, 20],
          ['Quang Tri', 1324110, 181.76],
          ['Hue', 959574, 117.27],
          ['Da Nang', 907563, 130.17],
          ['Ho Chi Minh', 655875, 10.9],
        ]}
        options={{
          region: 'VN',
          displayMode: 'markers',
          sizeAxis: { minValue: 0, maxValue: 100 },
          colorAxis: { colors: ['green', 'red'] },
        }}
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        mapsApiKey="AIzaSyBYRrNH2zytvjxNW0WpYpYv8aOJ1CXf35E"
        rootProps={{ 'data-testid': '3' }}
      />
    </div>
  );
};
