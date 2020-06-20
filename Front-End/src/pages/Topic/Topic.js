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
import { Nodata } from '../Nodata/Nodata';

export const Topic = () => {
  const [dataTopic, setDataTopic] = useState();
  const [dataTag, setDataTag] = useState();
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState(false);
  const [dataDetail, setDataDetail] = useState();
  const [err, setErr] = useState(false);
  const [displayTop, setDisplayTop] = React.useState(false);
  const [displayPost, setDisplayPost] = React.useState(false);
  const [dataPost, setDataPost] = React.useState();
  const [name, setName] = useState({ item: '', text: '' });

  /**
   * fetch data from 2 link
   */
  useEffect(() => {
    setLoading(true);
    setErr(false);
    let one = `${process.env.REACT_APP_LOCAL_URL}vnexpress/toptopic`;
    let two = `${process.env.REACT_APP_LOCAL_URL}vnexpress/toptag`;

    const requestOne = axios.get(one);
    const requestTwo = axios.get(two);

    axios
      .all([requestOne, requestTwo])
      .then(
        axios.spread((...responses) => {
          const responseOne = responses[0];
          const responseTwo = responses[1];
          console.log(responseOne);
          console.log(responseTwo);
          setDataTopic(getData(responseOne.data, 'Topic'));
          setDataTag(getData(responseTwo.data, 'Tag'));
          setLoading(false);
        })
      )
      .catch((errors) => {
        console.log('object');
        setErr(true);
        setLoading(false);
        alert('Oops, Something went wrong! Please try again.');
        console.log(errors);
      });
  }, []);

  /**
   * Format array data and return a new array
   * @param {Array} res A array data
   * @param {string} item Type of array data (topic or tag)
   */
  function getData(res, item) {
    return res.map((e) => ({
      id: e.id,
      text: e.title,
      value: e.count_posts,
      item: item,
    }));
  }

  /**
   * I dont know. I just copy on Stackoverflow
   * @param {*} word Word in worldCloud
   */
  const fontSizeMapper = (word) => Math.log2(word.value) * 5;

  const getReturnData = (e) => {
    console.log(e);
    let resData = dataDetail.sentiment_by_date.filter(
      (elems) => elems.date === e
    );
    setDataPost(resData[0]);
    setDisplayTop(false);
    setDisplayPost(true);
  };

  /**
   * Get event when click on word, then fetch API with word's id
   * @param {event} e
   */
  const handleChange = (e) => {
    console.log(e);
    let topicDetail = `${process.env.REACT_APP_LOCAL_URL}vnexpress/topicsentiment?idtopic=`;
    let tagDetail = `${process.env.REACT_APP_LOCAL_URL}vnexpress/tagsentiment?idtag=`;
    setLoading(true);
    setName({ item: e.item, text: e.text });
    axios
      .get((e.item === 'Topic' ? topicDetail : tagDetail) + e.id)
      .then((res) => {
        console.log(res.data);
        setDataDetail(res.data);
        setFilter(true);
        setDisplayTop(true);
        setDisplayPost(false);
        setLoading(false);
        document.getElementById('result').scrollIntoView();
      })
      .catch((err) => {
        alert('Oops, Something went wrong! Please try again.');
        setLoading(true);
        console.log(err);
      });
  };

  if (loading) {
    return <Loading />;
  } else if (err) {
    console.log(err);
    return <Nodata />;
  } else {
    return (
      <div>
        <h1 className="h1 title">Chủ đề nổi bật</h1>
        <div className="row">
          <div className="col-md-6">
            <div className="card">
              <h4 className="card-header">Chủ đề phổ biến</h4>
              <div className="card-body">
                <WordCloud
                  data={dataTopic}
                  width={1000}
                  fontSizeMapper={fontSizeMapper}
                  onWordClick={handleChange}
                />
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card">
              <h4 className="card-header">Tag phổ biến</h4>
              <div className="card-body">
                <WordCloud
                  data={dataTag}
                  width={1000}
                  fontSizeMapper={fontSizeMapper}
                  onWordClick={handleChange}
                />
              </div>
            </div>
          </div>
        </div>
        {filter ? (
          <div id="result" className="mt-5 result-detail">
            <div className="row mb-3">
              <div className="col-md-12">
                <h3>
                  {name.item}: {name.text}
                </h3>
              </div>
            </div>
            <div className="row">
              <div className="col-md-6 col-sm 12">
                <div className="card">
                  <h4 className="card-header">Tích cực và Tiêu cực</h4>
                  <div className="card-body">
                    <DonutChart
                      data={[dataDetail.total_pos, dataDetail.total_neg]}
                      labels={['Tích cực', 'Tiêu cực']}
                    />
                  </div>
                </div>
              </div>
              <div className="col-md-6 col-sm 12">
                <div className="card">
                  <h4 className="card-header">Phản ứng của xã hội</h4>
                  <div className="card-body">
                    <LineChart
                      onReturnData={getReturnData}
                      dataPost={dataDetail.sentiment_by_date.map((e) => {
                        return e.data.count_post;
                      })}
                      dataPos={dataDetail.sentiment_by_date.map((e) => {
                        return e.data.pos;
                      })}
                      dataNeg={dataDetail.sentiment_by_date.map((e) => {
                        return e.data.neg;
                      })}
                      labels={dataDetail.sentiment_by_date.map((e) => {
                        return e.date;
                      })}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-5">
              {(dataDetail.top_post == null && displayTop) ||
              (dataPost == null && displayPost) ? (
                <div>Không có bài viết</div>
              ) : displayTop ? (
                <h2>Bài viết tiêu biểu:</h2>
              ) : displayPost ? (
                <h2>Bài viết trong ngày {dataPost.date}:</h2>
              ) : (
                <div></div>
              )}
            </div>
            <div className="d-flex flex-column align-items-center">
              <div className="top-post">
                {(dataDetail.top_post == null && displayTop) ||
                (dataPost == null && displayPost) ? (
                  <div></div>
                ) : displayTop ? (
                  dataDetail.top_post.map((e, index) => {
                    return (
                      <PostDetail
                        key={index}
                        link={e.url}
                        title={e.title}
                        description={e.description}
                        thumbnailUrl={e.thumbnailUrl}
                      />
                    );
                  })
                ) : displayPost ? (
                  dataPost.data.posts.map((e, index) => {
                    return (
                      <PostDetail
                        key={index}
                        link={e.url}
                        title={e.title}
                        description={e.description}
                        thumbnailUrl={e.thumbnailUrl}
                      />
                    );
                  })
                ) : (
                  <div></div>
                )}
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
