import React from 'react';
import './Nodata.scss';
import NodataImg from '../../assets/img/image.png';

export const Nodata = () => {
  return (
    <div className=" noData">
      <div className="d-flex justify-content-center">
        <img alt="" src={NodataImg}></img>
      </div>
    </div>
  );
};
