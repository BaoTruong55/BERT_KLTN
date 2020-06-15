import React from 'react';
import './Homepage.scss';
import Img1 from '../../assets/img/homepage1.png';
import Img2 from '../../assets/img/homepage2.jpg';
import { useHistory } from 'react-router-dom';

const Homepage = () => {
  let history = useHistory();
  function handleClick() {
    history.push("/world");
  }
  return (
    <div>
      <div className="row homepage">
        <div className="tilt-in-fwd-bl col-md-4 col-sm-12 flex-column d-flex justify-content-center align-items-center">
          <img alt="" src={Img1} />
          <p>Project được lấy dữ liệu và phân tích từ trang web VnExpress.vn</p>
          <button type="button" onClick={handleClick} className="btn btnStart mt-3">
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
