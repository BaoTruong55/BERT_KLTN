import React, { useEffect, useState } from 'react';
import './Topic.scss';
import 'react-date-range/dist/styles.css'; // main style file
import 'react-date-range/dist/theme/default.css';
import './Topic.scss';
import axios from 'axios';
import { Loading } from '../../shared/Loading/Loading';
import WordCloud from 'react-d3-cloud';
import { PostDetail } from '../../shared/PostDetail/PostDetail';
import { LineChart } from '../Category/components/LineChart';
import { DonutChart } from '../Category/components/DonutChart';

export const Topic = () => {
  const [data, setData] = useState();
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState(false);
  const [dataTag, setDataTag] = useState();

  useEffect(() => {
    async function fetchMyAPI() {
      setLoading(true);
      let response = await axios
        .get('http://127.0.0.1:5000/vnexpress/toptopic')
        .then((res) => {
          // console.log(res.data);
          let dataFetch = [];
          res.data.map((e) => {
            return dataFetch.push({
              id: e.id,
              text: e.title,
              value: e.count_posts,
            });
          });
          console.log(dataFetch);
          setData(dataFetch);
          setLoading(false);
        })
        .catch((err) => {
          setLoading(false);
          // setError(true);
          alert('Oops, Something went wrong! Please try again.');
          console.log(err);
        });
    }
    fetchMyAPI();
  }, []);

  const fontSizeMapper = (word) => Math.log2(word.value) * 5;

  const handleChange = (e) => {
    console.log(e);
    setLoading(true);
    axios
      .get('http://127.0.0.1:5000/vnexpress/topicsentiment?idtopic=' + e.id)
      .then((res) => {
        console.log(res.data);
        setDataTag(res.data);
        setFilter(true);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
        alert('Oops, Something went wrong! Please try again.');
        console.log(err);
      });
  };

  if (loading) {
    return <Loading />;
  } else {
    return (
      <div>
        <h1 className="h1 title">Topic</h1>
        <div className="row">
          <div className="col-md-6">
            <div className="card">
              <h4 className="card-header">Popular Tag</h4>
              <div className="card-body">
                <WordCloud
                  data={data}
                  width={1000}
                  fontSizeMapper={fontSizeMapper}
                  onWordClick={handleChange}
                />
              </div>
            </div>
          </div>
          <div className="col-md-6"></div>
        </div>
        {filter ? (
          <div className="mt-5">
            <div className="row">
              <div className="col-md-6 col-sm 12">
                <div className="card">
                  <h4 className="card-header">Pos and Neg</h4>
                  <div className="card-body">
                    <DonutChart
                      data={[dataTag.total_pos, dataTag.total_neg]}
                      labels={['Positive', 'Negative']}
                    />
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-sm 12">
                <div className="card">
                  <h4 className="card-header">Reaction of society</h4>
                  <div className="card-body">
                    <LineChart
                      dataPos={dataTag.sentiment_by_date.map((e) => {
                        return e.data.pos;
                      })}
                      dataNeg={dataTag.sentiment_by_date.map((e) => {
                        return e.data.neg;
                      })}
                      labels={dataTag.sentiment_by_date.map((e) => {
                        return e.date;
                      })}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-5">
              <h2>Top post:</h2>
            </div>
            <div className="d-flex flex-column align-items-center">
              <div className="top-post">
                {dataTag.top_post.map((e, index) => {
                  return (
                    <PostDetail
                      key={index}
                      link={e.url}
                      title={e.title}
                      description={e.description}
                      thumbnailUrl={e.thumbnailUrl}
                    />
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          <div></div>
        )}
      </div>
    );
  }
};
