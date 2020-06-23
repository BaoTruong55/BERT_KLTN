import React, { useEffect, useState } from 'react';
import './World.scss';
import { ConfirmedCaseChart } from './Components/ConfirmedCaseChart';
import { CasesChart } from './Components/Cases';
import { GeoChart } from '../../shared/GeoChart/GeoChart';
import axios from 'axios';
import { Loading } from '../../shared/Loading/Loading';
import Paper from '@material-ui/core/Paper';
import { BarChart } from './Components/BarChart';
import { Nodata } from '../Nodata/Nodata';

export const World = () => {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(true);
  const [mapData, setMapData] = useState([]);
  const [error, setError] = React.useState(false);
  const [dataChart, setDataChart] = useState({
    growthName: [],
    growthValue: [],
    totalCases: [],
    recoveredCases: [],
    dayLabels: [],
    dayCases: [],
    dayRecovered: [],
  });

  /**
   * fetch data from website VnExpress
   */
  useEffect(() => {
    async function fetchMyAPI() {
      setLoading(true);
      await axios
        .get('https://gw.vnexpress.net/cr/?name=tracker_coronavirus')
        .then((res) => {
          // console.log(res.data.data);

          if (res.data && res.data.data && res.data.data.data[0]) {
            let tracker_by_province = res.data.data.data[0].tracker_by_province;
            let tracker_by_growth = res.data.data.data[0].tracker_by_growth;
            let tracker_by_day = res.data.data.data[0].tracker_by_day;

            if (tracker_by_province) {
              let mapDataTam = [];
              mapDataTam.push(['City', 'Cases', 'Area']);
              for (let i = 0; i < tracker_by_province.length; i++) {
                mapDataTam.push([
                  tracker_by_province[i].name,
                  tracker_by_province[i].cases,
                  tracker_by_province[i].cases,
                ]);
              }
              setMapData(mapDataTam);
            }

            if (tracker_by_growth && tracker_by_day) {
              let dataGrowthName = [];
              let dataGrowthValue = [];
              let dataRecovered = [];
              let dataTotalCases = [];
              let dataDayLabels = [];
              let dataDayCases = [];
              let dataDayRecovered = [];

              for (let i = 0; i < tracker_by_growth.length; i++) {
                dataGrowthName.push(tracker_by_growth[i].day);
                dataGrowthValue.push(
                  tracker_by_growth[i].cases - tracker_by_growth[i].recovered
                );
                dataTotalCases.push(tracker_by_growth[i].cases);
                dataRecovered.push(tracker_by_growth[i].recovered);
              }

              for (let i = 0; i < tracker_by_day.length; i++) {
                dataDayLabels.push(tracker_by_day[i].day);
                dataDayCases.push(tracker_by_day[i].cases);
                dataDayRecovered.push(tracker_by_day[i].recovered);
              }
              setDataChart({
                growthName: dataGrowthName,
                growthValue: dataGrowthValue,
                totalCases: dataTotalCases,
                recoveredCases: dataRecovered,
                dayLabels: dataDayLabels,
                dayCases: dataDayCases,
                dayRecovered: dataDayRecovered,
              });
            }
          }
          setData(res.data.data);
          setLoading(false);
        })
        .catch((err) => {
          setLoading(false);
          setError(true);
          alert('Oops, Something went wrong! Please try again.');
          console.log(err);
        });
    }
     fetchMyAPI();
  }, []);

  if (loading) {
    return <Loading />;
  } else {
    return (
      <div>
        <h1 className="h1 title">Việt Nam</h1>
        {error ? (
          <Nodata />
        ) : (
          <div>
            <div className="row">
              <div className="col-md-6">
                <div className="row">
                  <div className="col-md-4 mr-b">
                    <Paper
                      className="d-flex flex-column align-items-center pt-2"
                      elevation={3}
                    >
                      <h4>Ca nhiễm</h4>
                      <h3>{data.data[0].tracker_total_by_day.cases}</h3>
                    </Paper>
                  </div>
                  <div className="col-md-4 mr-b">
                    <Paper
                      className="d-flex flex-column align-items-center pt-2"
                      elevation={3}
                    >
                      <h4>Đang điều trị</h4>
                      <h3>
                        {data.data[0].tracker_total_by_day.cases -
                          data.data[0].tracker_total_by_day.recovered}
                      </h3>
                    </Paper>
                  </div>
                  <div className="col-md-4 mr-b">
                    <Paper
                      className="d-flex flex-column align-items-center pt-2"
                      elevation={3}
                    >
                      <h4>Khỏi</h4>
                      <h3>{data.data[0].tracker_total_by_day.recovered}</h3>
                    </Paper>
                  </div>
                </div>
                <Paper className="mt-3 pl-3 mr-b" elevation={3}>
                  <div className="row pt-2">
                    <div className="col-md-12">
                      <h3>Thống kê theo tỉnh thành</h3>
                    </div>
                  </div>
                  <div className="row covid-table table-responsive">
                    <div className="col-md-12 ">
                      <table className="table">
                        <thead>
                          <tr>
                            <th scope="col"></th>
                            <th scope="col">Nhiễm</th>
                            <th scope="col">Tử vong</th>
                            <th scope="col">Khỏi</th>
                          </tr>
                        </thead>
                        <tbody>
                          {data.data[0].tracker_by_province.map((e, index) => {
                            return (
                              <tr key={index}>
                                <th scope="row">{e.name}</th>
                                <td>{e.cases}</td>
                                <td>{e.deaths}</td>
                                <td>{e.recovered}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </Paper>
              </div>
              <div className="col-md-6 d-flex flex-column justify-content-center align-items-center case-chart">
                <h4>Phân bố ca nhiễm ở Việt Nam</h4>
                <GeoChart data={mapData} />
              </div>
            </div>

            <div className="row mt-5">
              <div className="col-md-12">
                <div className="card">
                  <h4 className="card-header">Số ca đang điều trị</h4>
                  <div className="card-body">
                    <CasesChart
                      data={dataChart.growthValue}
                      labels={dataChart.growthName}
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="row mt-5">
              <div className="col-md-6 col-sm-12 mb-4">
                <div className="card">
                  <h4 className="card-header">Tổng số ca</h4>
                  <div className="card-body">
                    <ConfirmedCaseChart
                      labels={dataChart.growthName}
                      data1={dataChart.totalCases}
                      data2={dataChart.recoveredCases}
                    />
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-sm-12 mb-4">
                <div className="card">
                  <h4 className="card-header">Số ca theo ngày</h4>
                  <div className="card-body">
                    <BarChart
                      labels={dataChart.dayLabels}
                      data1={dataChart.dayCases}
                      data2={dataChart.dayRecovered}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }
};
