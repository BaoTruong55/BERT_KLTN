import React from 'react';
import { Chart } from 'react-google-charts';

export const GeoChart = (props) => {
  return (
    <div>
      <Chart
        width={'1000px'}
        height={'700px'}
        chartType="GeoChart"
        data={props.data}
        options={{
          region: 'VN',
          displayMode: 'markers',
          colorAxis: { colors: ['green', 'red'] },
          backgroundColor: '#fff',
          datalessRegionColor: '#FFE6B3',
          defaultColor: '#f5f5f5',
          magnifyingGlass: { enable: true, zoomFactor: 7.5 },
          resolution: 'provinces',
          forceIFrame: true
        }}
        // Note: you will need to get a mapsApiKey for your project.
        // See: https://developers.google.com/chart/interactive/docs/basic_load_libs#load-settings
        mapsApiKey="AIzaSyBYRrNH2zytvjxNW0WpYpYv8aOJ1CXf35E"
        rootProps={{ 'data-testid': '3' }}
      />
    </div>
  );
};
