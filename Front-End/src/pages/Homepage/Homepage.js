import React from 'react';
import './Homepage.scss';
// import Img1 from '../../assets/img/homepage1.png';
import ImgTitle from '../../assets/img/title-homepage.png'
import Img2 from '../../assets/img/homepage2.jpg';
import { useHistory } from 'react-router-dom';

const Homepage = () => {
  let history = useHistory();
  function handleClick() {
    history.push('/vietnam');
  }
  return (
    <div>
      <div className="row homepage">
        <div className="tilt-in-fwd-bl col-md-4 col-sm-12 flex-column d-flex justify-content-center align-items-center mr-b">
          {/* <div className="title-homepage">
            <div className="row">
              <div className="col-md-12 title-homepage_Sa">
                Phân tích tình cảm
              </div>
            </div>
            <div className="row">
              <div className="col-md-4 d-flex">
                <div className="row">
                  <div className="col-md-12 title-homepage_comment">
                    bình luận
                  </div>
                  <div className="col-md-12 title-homepage_comment">về</div>
                </div>
              </div>
              <div className="col-md-8">
                <div className="row">
                  <div className="col-md-12 title-homepage_covid pl-0 pr-0">Covid-19</div>
                </div>
              </div>
            </div>
          </div> */}
          <img alt="" src={ImgTitle} className="img1" />
          <p className="description">Project được lấy dữ liệu và phân tích từ trang web VnExpress.vn</p>
          <button
            type="button"
            onClick={handleClick}
            className="btn btnStart mt-3"
          >
            Start
          </button>
        </div>
        <div className="tilt-in-fwd-br col-md-8 col-sm-12 d-flex justify-content-center align-items-center">
          <img alt="" src={Img2} className="img2" />
        </div>
      </div>
    </div>
  );
};

export default Homepage;
