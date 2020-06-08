import React from 'react';
import './World.scss';
import { ComfirmedCaseChart } from './Components/ComfirmedCaseChart';
import { DeathsChart } from './Components/DeathsChart';
import TableTop10 from './Components/TableTop10';
export const World = () => {
  return (
    <div>
      <h1 className="h1 title">World</h1>
      <div className="row">
        <div className="col-md-6 col-sm-12 mb-4">
          <div className="card">
            <h4 className="card-header">Confirmed cases</h4>
            <div className="card-body">
              <ComfirmedCaseChart />
            </div>
          </div>
        </div>
        <div className="col-md-6 col-sm-12 mb-4">
          <div className="card">
            <h4 className="card-header">Deaths</h4>
            <div className="card-body">
              <DeathsChart />
            </div>
          </div>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <h4>Top 10</h4>
          <TableTop10 />
        </div>
      </div>
    </div>
  );
};
